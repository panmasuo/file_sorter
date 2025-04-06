from enum import Enum
from pathlib import Path


class FileCategories(Enum):
    """Categories of the files that can be sorted into their separate
    directory."""
    PHOTO = "photo"
    VIDEO = "video"
    TRASH = "trash"


FILE_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".JPG"}
FILE_VIDEO_SUFFIXES = {".3gp", ".MPG", ".avi", ".mp4", ".MP4"}
RENAME_CATEGORIES = {FileCategories.PHOTO, FileCategories.VIDEO}


def get_file_category(file: Path) -> FileCategories:
    """Takes file and check its suffix against configured
    types. Returns class of the file based on that.

    Args:
        file (Path): File path.

    Returns:
        FileCategories: File class type.
    """
    if file.suffix in FILE_IMAGE_SUFFIXES:
        return FileCategories.PHOTO

    elif file.suffix in FILE_VIDEO_SUFFIXES:
        return FileCategories.VIDEO

    return FileCategories.TRASH
