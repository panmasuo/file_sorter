from pathlib import Path
import os
import shutil

from sorter.classifier import get_file_classifier, RENAME_CLASSES
from sorter.naming import create_name_and_date


class FileType:

    def __init__(self, file_path: Path):
        self._file = file_path
        self._file_class = get_file_classifier(self._file)
        self._generated_name, self._date = create_name_and_date(self._file)

    def __str__(self):
        return self._file.name

    def copy(self, target: Path) -> bool:
        target = self._create_destination(target)

        if not self._can_copy_and_rename(target):
            print(f"File '{self._file.name}' -> '{self._generated_name}' "
                  "already exist!")  # TODO: logger
            return False

        self._file = Path(shutil.copy2(self._file, target))
        return True

    def _create_destination(self, dst: Path) -> Path:
        # TODO: single responsibility!
        dst /= self._file_class.value

        dst /= str(self._date.year)

        os.makedirs(dst, exist_ok=True)

        if self._should_rename():
            dst /= self._generated_name

        return dst

    def _can_copy_and_rename(self, target: Path) -> bool:
        return not target.is_file()

    def _should_rename(self) -> bool:
        return self._file_class in RENAME_CLASSES