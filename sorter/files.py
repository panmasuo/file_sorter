from pathlib import Path

from sorter.classifier import get_file_classifier
from sorter.naming import create_name


class FileType:

    def __init__(self, file_path: Path):
        self._file = file_path
        self._file_class = get_file_classifier(self._file)
        self._generated_name = create_name(self._file)

    def __str__(self):
        return self._file.name

    def __repr__(self):
        return f"{self._file.name} {self._file_class} {self._generated_name}"

    def copy(self):
        self._file
        raise NotImplementedError

    def rename(self):
        try:
            self._file = self._file.rename(self._generated_name)
        except FileExistsError:
            # probably same file, do not override
            print(f"File {self} already exists")  # TODO: logger
        except PermissionError:
            print(f"Can't access file {self}")  # TODO: logger
