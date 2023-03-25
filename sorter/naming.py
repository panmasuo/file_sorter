from datetime import datetime
from pathlib import Path
from plum import exceptions
from typing import Tuple

from exif import Image
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from hachoir.core import config


def create_name_and_date(file_: Path) -> Tuple[str, datetime]:
    """Extracts date information from different sources,
    compares the dates then creating name using oldest
    date, timestamp and file suffix.

    Args:
        file_ (Path): File path.

    Returns:
        str: Name created from date and time.
    """
    # functions that can return datetime
    date_functions = [_meta_date, _hachoir_date, _exif_date]

    creation_dates = [creation for func in date_functions
                      if (creation := func(file_))]

    date = min(creation_dates)
    name = (date.strftime("%Y-%m-%d_%H-%M-%S") +
            f"_{int(date.timestamp())}" +  # a timestamp for uniqueness
            f"{file_.suffix}")

    return (name, date)


def _meta_date(file_: Path) -> datetime | None:
    """Gets date using file stat metadata."""
    create_time = file_.stat().st_ctime
    modify_time = file_.stat().st_mtime

    timestamp = min(create_time, modify_time)
    return datetime.fromtimestamp(timestamp)


def _hachoir_date(file_: Path) -> datetime | None:
    """Gets date using hachoir parser module."""
    config.quiet = True  # suppress annoying [warn] log message

    try:
        if (parser := createParser(file_)) is None:
            return

        metadata = extractMetadata(parser)
        for line in metadata.exportPlaintext():
            if '- Creation date' in (created := line.split(':')):
                date_str = f"{created[1]}:{created[2]}:{created[3]}"
                return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    except AttributeError:
        # raised on InputPipe object without "close" attribute
        pass


def _exif_date(file_: Path) -> datetime | None:
    """Gets date using exif metadata."""
    try:
        exif_image = Image(file_)
        if exif_image.has_exif:
            return datetime.strptime(exif_image.datetime, '%Y:%m:%d %H:%M:%S')

    except AttributeError:
        # called on exif objects without datetime attribute
        pass

    except exceptions.UnpackError:
        # called on while unpacking
        pass
