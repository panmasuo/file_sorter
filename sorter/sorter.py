from pathlib import Path

from sorter.files import FileType
from sorter.classifier import FileClassifier


class Sorter:
    """Sorter class responsible for creating sorting categories (directories),
    file paths and tracking progress.
    """

    def __init__(self, source_path: str, destination_path: str):
        """Creates paths for source and destination directories then
        creates file lists and sorting categories."""
        self.source = Path(source_path)
        self.destination = Path(destination_path)

        self._create_files_list()
        self._make_file_class_directiories()

    def get_files(self) -> Path:
        """Yields file paths."""
        for file in self._files:
            yield file

    def files_size(self) -> None:
        """Return size (length) of file list."""
        return len(self._files)

    def _create_files_list(self) -> None:
        """Traverse all paths in source directory and set list with
        all files. Directories and other links are not listed.
        """
        paths = self.source.glob('**/*')
        self._files = [FileType(Path(path)) for path in paths
                       if path.is_file()]

    def _make_file_class_directiories(self) -> bool:
        """Creates directories for sorting, using FileClassifier."""
        for file_class in FileClassifier:
            Path(self.destination / file_class.value).mkdir(exist_ok=True)
