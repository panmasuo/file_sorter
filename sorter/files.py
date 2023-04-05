import logging
from pathlib import Path
import os
import shutil

from sorter.categories import get_file_category, RENAME_CATEGORIES
from sorter.naming import create_name_and_date

log = logging.getLogger(__name__)


class FileType:

    def __init__(self, file_path: Path):
        self._file = file_path
        self._file_class = get_file_category(self._file)
        self._generated_name, self._date = create_name_and_date(self._file)

    def __str__(self):
        return self._file.name

    def copy(self, target: Path) -> bool:
        target = self._create_destination(target)

        if not self._can_copy_and_rename(target):
            log.warn(f"File '{self._file.name}' -> '{self._generated_name}' "
                     "already exist!")
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
        return self._file_class in RENAME_CATEGORIES
