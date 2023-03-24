from pathlib import Path
import shutil

from sorter.classifier import get_file_classifier
from sorter.naming import create_name


class FileType:

    def __init__(self, file_path: str):
        self._file = Path(file_path)
        self._file_class = get_file_classifier(self._file)
        self._generated_name = create_name(self._file)

    def __str__(self):
        return self._file.name

    def __repr__(self):
        return f"{self._file.name} {self._file_class} {self._generated_name}"

    def copy(self, target_dir: str) -> bool:
        if not self._can_copy_and_rename(target_dir):
            print(f"File {self._generated_name} already exist!")  # TODO: logger
            return False

        self._file = Path(shutil.copy2(self._file, target_dir))
        return True

    def rename(self):
        # try:
        self._file = self._file.rename(self._generated_name)
        # except PermissionError:
            # TODO: does it actually happen? if yes, we should just stop
            # print(f"Can't access file {self}")  # TODO: logger

    def _can_copy_and_rename(self, target_dir: str) -> bool:
        target_path = Path(target_dir) / self._generated_name
        return not target_path.is_file()
