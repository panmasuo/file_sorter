from sorter.directories import get_directory_path
from sorter.sorter import Sorter


if __name__ == "__main__":
    src = get_directory_path("Select media source directory")
    dst = get_directory_path("Select sorted media destination directory")

    sorter = Sorter(src, dst)
    total_count = sorter.files_size()

    for i, _file in enumerate(sorter.get_files()):
        print(f"Progress {i} / {total_count}")  # TODO: logger

        _file.copy(sorter.destination)
