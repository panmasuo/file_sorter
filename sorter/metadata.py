from datetime import datetime
from pathlib import Path
from plum import exceptions
from typing import Any, Tuple
import logging

from exif import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from hachoir.stream.input import NullStreamError, InputStreamError

# imports for loggers
from exif._image import logger as exif_logger
from hachoir.core import config as hachor_logger

hachor_logger.quiet = True  # suppress hachoir log messages

# TODO any suppresing of the exif is not working
# exif_logger.setLevel(logging.CRITICAL)  # suppress exif log messages
for handler in exif_logger.handlers[:]:
    exif_logger.removeHandler(handler)


log = logging.getLogger(__name__)


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

    # take oldest timestamp - to be sure it is the real one, remove 1980-01-01
    timestamps = list(filter(lambda x: x != 315529200000000000, timestamps))
    timestamp = min(timestamps)

    date = datetime.fromtimestamp(timestamp // 1000000000)
    # e.g. 2005-04-02_16000000000.jpg
    name = (date.strftime("%Y-%m-%d") + f"_{timestamp}" + f"{file.suffix}")
    return (name, date)


def _meta_date(file: Path) -> int | None:
    """Gets date using file stat metadata."""
    create_time = file.stat().st_ctime_ns
    modify_time = file.stat().st_mtime_ns

    ns_timestamp = min(create_time, modify_time)
    return ns_timestamp


def _hachoir_date(file: Path) -> int | None:
    """Gets date using hachoir parser module."""
    try:
        if (parser := createParser(f"{file}")) is None:
            return

        metadata = extractMetadata(parser)
        date = metadata.get("creation_date", 0)

    except (AttributeError, NullStreamError, InputStreamError) as e:
        # AttributeError raised on InputPipe object without "close" attribute
        # InputStreamError raised when trying to open directories
        log.debug(e)
        return

    if (timestamp := _convert_date_to_timestamp(date)):
        ns_timestamp = _create_ns_timestamp(timestamp, 0)
        return ns_timestamp


def _exif_date(file: Path) -> int | None:
    """Gets date using exif metadata."""
    try:
        exif = Image(file)
        if exif.has_exif:
            date = exif.get("datetime_original")
            subsecond = exif.get("subsec_time_original", 0)
        else:
            return

    except (exceptions.UnpackError, ValueError, RuntimeWarning) as e:
        # called on while unpacking
        log.debug(e)
        return

    if not (timestamp := _convert_date_to_timestamp(date)):
        return

    if isinstance(subsecond, str):
        subsecond = int(subsecond)

    ns_timestamp = _create_ns_timestamp(timestamp, subsecond)

    return ns_timestamp


def _convert_date_to_timestamp(date: Any) -> str | None:
    if not date:
        return None

    if isinstance(date, str):
        date = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")

    try:
        # cast to int to remove decimals
        timestamp = int(date.timestamp())
    except (AttributeError, OSError) as e:
        log.debug(e)
        return None

    return f"{timestamp}"


def _create_ns_timestamp(timestamp: str, nanoseconds: int = 0) -> int:
    # filling with zeroes will make the timestamp work as nanosecond timestamp
    return int(f"{timestamp}{nanoseconds:<09d}")
