from sorter.directories import get_directory_path
from sorter.sorter import Sorter

src = get_directory_path("Source directory")
dst = get_directory_path("Destination directory")

sorter = Sorter(src, dst)
for _file in sorter.get_files():
    if _file.copy(sorter.destination):
        _file.rename()
