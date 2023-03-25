from pathlib import Path
import shutil

from sorter.classifier import get_file_classifier, RENAME_CLASSES
from sorter.naming import create_name


class FileType:

    def __init__(self, file_path: Path):
        self._file = file_path
        self._file_class = get_file_classifier(self._file)
        self._generated_name = create_name(self._file)

    def __str__(self):
        return self._file.name

    def copy(self, target: Path) -> bool:
        target /= self._file_class.value

        if self._should_rename():
            target /= self._generated_name

        if not self._can_copy_and_rename(target):
            print(f"File '{self._file.name}' -> '{self._generated_name}' "
                  "already exist!")  # TODO: logger
            return False

        self._file = Path(shutil.copy2(self._file, target))
        return True

    def _can_copy_and_rename(self, target: Path) -> bool:
        return not target.is_file()

    def _should_rename(self) -> bool:
        return self._file_class in RENAME_CLASSES
