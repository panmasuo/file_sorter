from enum import Enum
from pathlib import Path

FILE_IMAGE_SUFFIXES = [".jpg", ".jpeg", ".JPG"]
FILE_VIDEO_SUFFIXES = [".3gp", ".MPG", ".avi", ".mp4", ".MP4"]


class FileClasifier(Enum):
    PHOTO = "photo"
    VIDEO = "video"
    TRASH = "trash"


def get_file_classifier(file_: Path) -> FileClasifier:
    """Takes file and check its suffix against configured
    types. Returns class of the file based on that.

    Args:
        file_ (Path): File path.

    Returns:
        FileClasifier: File class type.
    """
    if file_.suffix in FILE_IMAGE_SUFFIXES:
        return FileClasifier.PHOTO

    elif file_.suffix in FILE_VIDEO_SUFFIXES:
        return FileClasifier.VIDEO

    return FileClasifier.TRASH
