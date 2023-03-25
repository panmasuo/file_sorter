from enum import Enum
from pathlib import Path


class FileClassifier(Enum):
    PHOTO = "photo"
    VIDEO = "video"
    TRASH = "trash"


FILE_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".JPG"}
FILE_VIDEO_SUFFIXES = {".3gp", ".MPG", ".avi", ".mp4", ".MP4"}
RENAME_CLASSES = {FileClassifier.PHOTO, FileClassifier.VIDEO}


def get_file_classifier(file_: Path) -> FileClassifier:
    """Takes file and check its suffix against configured
    types. Returns class of the file based on that.

    Args:
        file_ (Path): File path.

    Returns:
        FileClassifier: File class type.
    """
    if file_.suffix in FILE_IMAGE_SUFFIXES:
        return FileClassifier.PHOTO

    elif file_.suffix in FILE_VIDEO_SUFFIXES:
        return FileClassifier.VIDEO

    return FileClassifier.TRASH
