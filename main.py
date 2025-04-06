import logging
import sys

# configure logging before anything else
logging.basicConfig(
    filename="logs.log",
    filemode='a',
    level=logging.DEBUG,
    format="[%(levelname)s %(name)s:%(lineno)d] [%(thread)d] %(message)s"
)

log = logging.getLogger("main")

from duplicate_images.duplicate import main as di_main

from sorter.directories import get_directory_path
from sorter.sorter import Sorter


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
