from sorter.files import FileType


class Sorter:

    def __init__(self, source_path: str, destination_path: str):
        self.source = source_path
        self.destination = destination_path

    def get_files(self):
        all_paths = self.source.glob('**/*')
        return [FileType(path) for path in all_paths if path.is_file()]
