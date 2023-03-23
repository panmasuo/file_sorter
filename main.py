from sorter.directories import get_directory_path
from sorter.files import FileType

dir = get_directory_path("Source directory")

files = dir.glob('**/*')
for _file in files:
    # print(_file)
    if _file.is_file():
        print(repr(FileType(_file)))
