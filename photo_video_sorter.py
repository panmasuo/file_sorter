from datetime import datetime
from exif import Image
from pathlib import Path
from tkinter.filedialog import askdirectory

import shutil

class Sorter:
    __slots__ = ["source_dir", "destination_dir", "image_suffix",
                 "video_suffix"]
    def __init__(self):
        self.image_suffix = [".jpg", ".jpeg", ".JPG"]
        self.video_suffix = [".3gp", ".MPG", ".avi", ".mp4"]

    def get_source_dir(self):
        source_directory = askdirectory()
        # source_directory = "D:/from"
        self.source_dir = Path(source_directory)

    def get_destination_dir(self):
        destination_directory = askdirectory()
        # destination_directory = "D:/to"
        self.destination_dir = Path(destination_directory)

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
        self._set_creation_time()
        self._expand_destination_directory_by_bin()
        self._create_new_name()

    def copy(self):
        dst_file = Path(Path(self.destination_dir) / self.new_name)
        if not dst_file.is_file():
            shutil.copy2(self._file, self.destination_dir)
            self._file = Path(self.destination_dir) / self._file.name
        else:
            return

    def rename(self):
        try:
            Path.rename(self._file, self._file.parent / self.new_name)
        except FileExistsError:
            pass  # file already exists, do not override

    def _create_new_name(self):
        self.new_name = (f"{self.create_time.month:02d}-{self.create_time.day:02d}_"
                    f"{self.create_time.hour:02d}-{self.create_time.minute:02d}-"
                    f"{self.create_time.second:02d}{self._file.suffix}")

    def _set_creation_time(self):
        create_time = self._file.stat().st_ctime
        modify_time = self._file.stat().st_mtime
        # always pick older date
        self.timestamp = create_time if create_time < modify_time else modify_time
        self.create_time = datetime.fromtimestamp(self.timestamp)

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
        self._set_creation_time()
        self._expand_destination_directory_by_year()

    def _set_creation_time(self):
        exif_image = Image(self._file)

        try:
            if exif_image.has_exif:
                self.create_time = datetime.strptime(exif_image.datetime, '%Y:%m:%d %H:%M:%S')
                self.timestamp = self.create_time.timestamp
                return
            else:
                raise AttributeError
        except AttributeError:
            FileHandler._set_creation_time(self)


class Video(FileHandler):
    bin_folder_name = "videos"

    def __init__(self, _file, destination_dir):
        super().__init__(_file, destination_dir)
        self._set_creation_time()
        self._expand_destination_directory_by_year()


class Trash(FileHandler):
    bin_folder_name = "trash"

    def __init__(self, _file, destination_dir):
        super().__init__(_file, destination_dir)
        self._set_creation_time()
        self._expand_destination_directory_by_year()

    def rename(self):
        pass  # do not rename Trash file

sorter = Sorter()
sorter.get_source_dir()
sorter.get_destination_dir()
for _file in sorter.get_classified_file():
    _file.copy()
    _file.rename()
