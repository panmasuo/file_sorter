import logging
from pathlib import Path
import os
import shutil

from sorter.categories import get_file_category, RENAME_CATEGORIES
from sorter.naming import create_name_and_date

log = logging.getLogger(__name__)


class FileType:

    def __init__(self, file_path: Path):
        self._duplicated = False

        self._file = file_path
        self._file_class = get_file_category(self._file)
        self._generated_name, self._date = create_name_and_date(self._file)

    def __str__(self):
        return self._file.name

    def copy(self, target: Path) -> bool:
        target = self._create_destination(target)

        if not self._can_copy_and_rename(target):
            self._set_duplicate(target)

            log.debug(f"File '{self._file.absolute()}' -> '{target}' "
                      "already exist!")
            return False

        try:
            self._file = Path(shutil.copy2(self._file, target))
        except PermissionError as e:
            log.error(f"file not copied: {e}")

        return True

    def rename_duplicate(self) -> None:
        if not self._duplicated:
            return

        i = 1
        while not self._can_copy_and_rename(self._dup_target):
            rename = (self._dup_target.stem[:-1] +
                      f"{i}" + f"{self._file.suffix}")

            try:
                self._dup_target.rename(self._dup_target.parent.absolute() /
                                        rename)
            except FileExistsError:
                i += 1

        self._generated_name = self._dup_target.name
        log.debug(f"created new destination for duplicate {self._dup_target}"
                  f": {self._generated_name}")

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

    def _set_duplicate(self, target: Path) -> None:
        self._duplicated = True

        self._dup_target = target

    def _should_rename(self) -> bool:
        return self._file_class in RENAME_CATEGORIES
