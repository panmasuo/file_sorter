from datetime import datetime
from pathlib import Path
from plum import exceptions
from typing import Tuple

from exif import Image
from hachoir.core import config
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from hachoir.stream.input import NullStreamError


def create_name_and_date(file: Path) -> Tuple[str, datetime]:
    """Extracts timestamp information from different sources,
    compares the dates then creating name using oldest
    date, timestamp and file suffix.

    Args:
        file (Path): File path.

    Returns:
        str: Name created from date and time.
    """
    # functions that can return nanoseconds timestamps
    date_functions = [_meta_date, _hachoir_date, _exif_date]

    timestamps = [timestamp for func in date_functions
                  if (timestamp := func(file))]

    timestamp = min(timestamps)
    date = datetime.fromtimestamp(timestamp // 1000000000)
    name = (date.strftime("%Y-%m-%d") + f"_{timestamp}" + f"{file.suffix}")

    return (name, date)


def _meta_date(file: Path) -> int | None:
    """Gets date using file stat metadata."""
    create_time = file.stat().st_ctime_ns
    modify_time = file.stat().st_mtime_ns

    return min(create_time, modify_time)


def _hachoir_date(file: Path) -> int | None:
    """Gets date using hachoir parser module."""
    config.quiet = True  # suppress log messages

    try:
        if (parser := createParser(f"{file}")) is None:
            return

        metadata = extractMetadata(parser)
        date = metadata.get("creation_date", 0)

        if not date:
            return None

        if not isinstance(date, datetime):
            dt = datetime.strptime(f"{date}", "%Y:%m:%d %H:%M:%S")

        dt = date
        # cast to int to cast away floatness
        try:
            timestamp = int(dt.timestamp())
        except Exception:
            return

        # TODO: redo
        filler = 0

        return int(f"{timestamp}{filler:<09d}")

    except AttributeError:
        # raised on InputPipe object without "close" attribute
        pass

    except NullStreamError:
        pass


def _exif_date(file: Path) -> int | None:
    """Gets date using exif metadata."""
    try:
        exif = Image(file)
        if exif.has_exif:
            date = exif.get("datetime_original")
            subsecond = exif.get("subsec_time_original", 0)

            if not date:
                return None

            if isinstance(date, str):
                date = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")

            timestamp = int(date.timestamp())

            if isinstance(subsecond, str):
                subsecond = int(subsecond)

            # create nanoseconds timestamp, fill missing zeroes if needed
            return int(f"{timestamp}{subsecond:<09d}")

    except exceptions.UnpackError:
        # called on while unpacking
        pass
