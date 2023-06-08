from concurrent.futures import ProcessPoolExecutor
from itertools import repeat
from multiprocessing import cpu_count
from pathlib import Path
from typing import Tuple, List
import logging

from sorter.files import FileType
from sorter.categories import FileCategories
from sorter.picker import Picker

log = logging.getLogger(__name__)


def _create_and_copy(target: Tuple[Path, Path]) -> List[FileType]:
    """Classify FileType and copy it to the destination.

    Args:
        target (Tuple[Path, Path]): Tuple of file path and its
            copy destination.

    Returns:
        List[FileType]: List of all the files.
    """
    path, dst = target
    file = FileType(path)
    file.copy(dst)
    return file


class Sorter:
    """Sorter class responsible for creating sorting categories (directories),
    file paths and tracking progress.
    """
    def __init__(self, source_path: str, destination_path: str):
        """Creates paths for source and destination directories then
        creates file lists and sorting categories."""
        self.source = Path(source_path)
        self.destination = Path(destination_path)

        self._create_paths_list()
        self._make_category_directiories()

    def sort(self) -> None:
        """Sorts files based on their file type and moves them to their
        corresponding destination directories. This method uses
        multiple processes.
        """
        result = None

        with ProcessPoolExecutor((cpu := cpu_count())) as executor:
        # with ProcessPoolExecutor(1) as executor:
            log.info(f"using {cpu} cpu cores")
            result = executor.map(
                _create_and_copy,
                zip(self._get_files(), repeat(self.destination))
            )

        picker = Picker()
        for file in result:
            if not file._duplicated:
                continue

            if "c" == picker.compare(file):
                # force rename
                file.rename_duplicate()
                # copy again
                file.copy(self.destination)

    def _get_files(self) -> Path:
        """Yields file paths."""
        for file in self._paths:
            yield Path(file)

    def _create_paths_list(self) -> None:
        """Traverse all paths in source directory and set list with
        all files. Directories and other links are not listed.
        """
        self._paths = self.source.glob('**/*')

    def _make_category_directiories(self) -> None:
        """Creates directories for sorting, using FileCategories."""
        for category in FileCategories:
            Path(self.destination / category.value).mkdir(exist_ok=True)
