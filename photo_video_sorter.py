from datetime import datetime
from exif import Image
from pathlib import Path
import shutil


class Sorter:
    __slots__ = ["source_dir", "destination_dir", "image_suffix",
                 "video_suffix"]
    def __init__(self):
        self.image_suffix = [".jpg", ".JPG"]
        self.video_suffix = [".MPG", ".avi"]

    def get_source_dir(self):
        # TODO input destination by user
        temp_destination = "D://from/"
        self.source_dir = Path(temp_destination)

    def get_destination_dir(self):
        # TODO input destination by user
        temp_destination = "D://to/"
        self.destination_dir = Path(temp_destination)

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
        self._expand_destination_directory_by_bin()

    def copy(self):
        shutil.copy2(self._file, self.destination_dir)
        self._file = Path(self.destination_dir) / self._file.name

    def rename(self):
        # TODO catch file existing
        new_name = (f"{self.create_time.month}-{self.create_time.day}_"
                    f"{self.create_time.hour}-{self.create_time.minute}-"
                    f"{self.create_time.second}{self._file.suffix}")
        try:
            Path.rename(self._file, self._file.parent / new_name)
        except FileExistsError:
            pass  # file already exists, do not override

    def _set_creation_time(self):
        self.timestamp = self._file.stat().st_ctime
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
        self.create_time = datetime.strptime(Image(self._file).datetime,
                                             '%Y:%m:%d %H:%M:%S')
        self.timestamp = self.create_time.timestamp


class Video(FileHandler):
    bin_folder_name = "videos"

    def __init__(self, _file, destination_dir):
        super().__init__(_file, destination_dir)
        self._set_creation_time()
        self._expand_destination_directory_by_year()


class Trash(FileHandler):
    def __init__(self, _file, destination_dir):
        super().__init__(_file, destination_dir)
        self._set_creation_time()
        self._expand_destination_directory_by_year()

sorter = Sorter()
sorter.get_source_dir()
sorter.get_destination_dir()
for _file in sorter.get_classified_file():
    _file.copy()
    _file.rename()
