from datetime import datetime
from pathlib import Path
from plum import exceptions
from typing import Any, Tuple

from exif import Image
from hachoir.core import config
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from hachoir.stream.input import NullStreamError

config.quiet = True  # suppress hachoir log messages


def create_name_and_date(file: Path) -> Tuple[str, datetime]:
    """Extracts timestamp information from different sources,
    compares the dates then creating name using oldest
    date, timestamp and file suffix.

    Args:
        file (Path): File path.

    Returns:
        Tuple[str, datetime]: Tuple of generated name and
            datetime object.
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

    try:
        if (parser := createParser(f"{file}")) is None:
            return

        metadata = extractMetadata(parser)
        date = metadata.get("creation_date", 0)

    except AttributeError:
        # raised on InputPipe object without "close" attribute
        return

    except NullStreamError:
        return

    if (timestamp := _convert_date_to_timestamp(date)):
        return _create_ns_timestamp(timestamp, 0)


def _exif_date(file: Path) -> int | None:
    """Gets date using exif metadata."""
    try:
        exif = Image(file)
        if exif.has_exif:
            date = exif.get("datetime_original")
            subsecond = exif.get("subsec_time_original", 0)
        else:
            return

    except exceptions.UnpackError:
        # called on while unpacking
        return

    if not (timestamp := _convert_date_to_timestamp(date)):
        return

    if isinstance(subsecond, str):
        subsecond = int(subsecond)

    return _create_ns_timestamp(timestamp, subsecond)


def _convert_date_to_timestamp(date: Any) -> str | None:
    if not date:
        return None

    if isinstance(date, str):
        date = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")

    # TODO: what if we have decimal value? we don't want to lose that
    try:
        # cast to int to remove decimals
        timestamp = int(date.timestamp())
    except AttributeError:
        return None
    except OSError:
        # TODO: see what is that
        return None

    return f"{timestamp}"


def _create_ns_timestamp(timestamp: str, nanoseconds: int = 0) -> int:
    nanoseconds = 0
    return int(f"{timestamp}{nanoseconds:<09d}")
