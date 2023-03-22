from datetime import datetime
from exif import Image
from pathlib import Path
from tkinter.filedialog import askdirectory

from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from hachoir.stream.input import NullStreamError

import os
import shutil

from sorter.directories import get_directory


class Sorter:
    def __init__(self):
        self.image_suffix = [".jpg", ".jpeg", ".JPG"]
        self.video_suffix = [".3gp", ".MPG", ".avi", ".mp4", ".MP4"]

    def count_files(self):
        count = 0
        for _, _, files in os.walk(str(self.source_dir)):
            for _ in files:
                count += 1
        return count

    def get_source_dir(self):
        self.source_dir = get_directory("Pick source directory")

    def get_destination_dir(self):
        self.destination_dir = get_directory("Pick destination directory")

    def get_classified_file(self):
        files = self.source_dir.glob('**/*')
        for _file in files:
            if _file.is_file():
                yield self.create_object_by_suffix(_file)

    def create_object_by_suffix(self, _file):
        if _file.suffix in self.image_suffix:
            return Photo(_file, self.destination_dir)

        elif _file.suffix in self.video_suffix:
            return Video(_file, self.destination_dir)

        else:
            return Trash(_file, self.destination_dir)


class FileHandler:
    bin_folder_name = "default"

    def __init__(self, _file, destination_dir):
        self._file = _file
        self.destination_dir = destination_dir
        self._get_file_create_or_modify_time()
        self._expand_destination_directory_by_bin()

    def copy(self):
        dst_file = Path(Path(self.destination_dir) / self.new_name)
        if dst_file.is_file():
            print(f"Files {self._file.name} destiny {str(dst_file)} exists!")
        else:
            shutil.copy2(self._file, self.destination_dir)
            self._file = Path(self.destination_dir) / self._file.name

    def rename(self):
        try:
            Path.rename(self._file, self._file.parent / self.new_name)
        except FileExistsError:
            print(f"File with name: {self._file.name} already exists!")
            # pass  # file already exists, do not override
        except PermissionError:
            print(f"Can't access this file {self._file.name}")

    def _create_new_name(self):
        self.new_name = (f"{self.create_time.month:02d}-{self.create_time.day:02d}_"
                        f"{self.create_time.hour:02d}-{self.create_time.minute:02d}-"
                        f"{self.create_time.second:02d}_{int(self.timestamp)}"
                        f"{self._file.suffix}")

    def _get_file_create_or_modify_time(self):
        create_time = self._file.stat().st_ctime
        modify_time = self._file.stat().st_mtime

        # always pick older date
        self.timestamp = create_time if create_time < modify_time else modify_time
        self.create_time = datetime.fromtimestamp(self.timestamp)
        self.time_source = "meta"

    def _get_media_creation_time(self):
        # https://gist.github.com/nikomiko/7492e5e82791c9ff989e2573ca180273
        try:
            if (parser := createParser(str(self._file))) is None:
                # print("cant get parser")
                return

            metadata = extractMetadata(parser)

            for line in metadata.exportPlaintext():
                if '- Creation date' in (creation_date := line.split(':')):
                    date_string = f"{creation_date[1]}:{creation_date[2]}:{creation_date[3]}"
                    create_time = datetime.strptime(date_string, " %Y-%m-%d %H:%M:%S")
                    if create_time < self.create_time:
                        try:
                            self.timestamp = create_time.timestamp()
                            self.create_time = create_time
                            self.time_source = "parser"
                        except OSError as e:  # windows timestamp is wrong
                            print(e)
        except AttributeError:
            print("cant get parser111")
        except TypeError as e:
            print(e)
        except NullStreamError as e:
            print(e)

    def _expand_destination_directory_by_bin(self):
        self.destination_dir = self.destination_dir / self.bin_folder_name
        try:
            self.destination_dir.mkdir()
        except FileExistsError:
            pass  # year folder already exists

    def _expand_destination_directory_by_year(self):
        year = self.create_time.year
        self.destination_dir = self.destination_dir / str(year)
        try:
            self.destination_dir.mkdir()
        except FileExistsError:
            pass  # year folder already exists


class Photo(FileHandler):
    bin_folder_name = "photos"

    def __init__(self, _file, destination_dir):
        super().__init__(_file, destination_dir)
        self._get_exif_time()
        self._expand_destination_directory_by_year()
        self._create_new_name()

    def _get_exif_time(self):
        exif_image = Image(self._file)

        try:
            if exif_image.has_exif:
                create_time = datetime.strptime(exif_image.datetime, '%Y:%m:%d %H:%M:%S')
                timestamp = create_time.timestamp()

                if create_time < self.create_time:
                    self.create_time = create_time
                    self.timestamp = timestamp
                    self.time_source = "exif"

                return
            else:
                raise AttributeError
        except AttributeError:
            pass
            # TODO exif not working always, use Video creation time function as well before default one


class Video(FileHandler):
    bin_folder_name = "videos"

    def __init__(self, _file, destination_dir):
        super().__init__(_file, destination_dir)
        self._get_media_creation_time()
        self._expand_destination_directory_by_year()
        self._create_new_name()


class Trash(FileHandler):
    bin_folder_name = "trash"

    def __init__(self, _file, destination_dir):
        super().__init__(_file, destination_dir)
        self._get_media_creation_time()
        self._expand_destination_directory_by_year()
        self._create_new_name()

    def rename(self):
        pass  # do not rename Trash file


sorter = Sorter()
sorter.get_source_dir()
sorter.get_destination_dir()

print(sorter.source_dir)
print(sorter.destination_dir)
# total_count = sorter.count_files()

# for i, _file in enumerate(sorter.get_classified_file()):
#     print("Progress: " + str(i) + "/" + str(total_count - 1))
#     _file.copy()
#     _file.rename()
#     # print(_file.time_source)
