import logging
import sys

from sorter.directories import get_directory_path
from sorter.sorter import Sorter

from duplicate_images.duplicate import main as di_main

log = logging.getLogger("main")


if __name__ == '__main__':
    print("Picking source and destination directories")

    src = get_directory_path("Select media source directory")
    dst = get_directory_path("Select sorted media destination directory")

    sorter = Sorter(src, dst)

    print("Started sorting...")
    sorter.sort()

    # use duplicate_images module
    # hardcode argparse arguments before calling duplicate_images
    # "call find_dups -h" for more info
    sys.argv[1:] = ["--on-equal", "delete-smallest", f"{dst}"]
    print("Starting duplicate images module...")
    di_main()
