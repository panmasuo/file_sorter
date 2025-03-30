import logging
import sys

from duplicate_images.duplicate import main as di_main

from sorter.directories import get_directory_path
from sorter.sorter import Sorter

# configure logging before anything else
logging.basicConfig(level=logging.INFO,
                    format="[%(levelname)s %(name)s:%(lineno)d] %(message)s")
log = logging.getLogger("main")


if __name__ == '__main__':
    log.warning("Picking source and destination directories")

    src = get_directory_path("Select media source directory")
    dst = get_directory_path("Select sorted media destination directory")

    sorter = Sorter(src, dst)
    sorter.sort()

    # use duplicate_images module
    # hardcode argparse arguments before calling duplicate_images
    # "call find_dups -h" for more info
    # sys.argv[1:] = ["--on-equal", "delete-smallest", f"{dst}"]
    # di_main()
