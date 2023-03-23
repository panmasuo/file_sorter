from datetime import datetime
from pathlib import Path

from exif import Image
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from hachoir.stream.input import NullStreamError


def create_name(file_: Path) -> str:
    name_functions = [_meta_name, _parser_name, _exif_name]

    creation_times = [creation for func in name_functions
                      if (creation := func(file_))]
    return min(creation_times)


def _meta_name(file_: Path) -> datetime | None:
    create_time = file_.stat().st_ctime
    modify_time = file_.stat().st_mtime

    timestamp = min(create_time, modify_time)
    return datetime.fromtimestamp(timestamp)


def _parser_name(file_: Path) -> datetime | None:
    # https://gist.github.com/nikomiko/7492e5e82791c9ff989e2573ca180273
    try:
        if (parser := createParser(file_)) is None:
            return

        metadata = extractMetadata(parser)
        for line in metadata.exportPlaintext():
            if '- Creation date' in (create_time := line.split(':')):
                date_str = f"{create_time[1]}:{create_time[2]}:{create_time[3]}"
                return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            # if create_time < create_time:
            #     try:
            #         timestamp = create_time.timestamp()
            #         create_time = create_time
            #         time_source = "parser"
            #     except OSError as e:  # windows timestamp is wrong
                    # print(e)
    except AttributeError as e:
        # print(f"excetion1 {e}")
        pass
    except TypeError as e:
        # print(f"excetion2 {e}")
        pass
    except NullStreamError as e:
        # print(f"excetion3 {e}")
        pass


def _exif_name(file_: Path) -> datetime | None:

    try:
        exif_image = Image(file_)
        if exif_image.has_exif:
            return datetime.strptime(exif_image.datetime, '%Y:%m:%d %H:%M:%S')
    #         timestamp = create_time.timestamp()

    #         if create_time < self.create_time:
    #             self.create_time = create_time
    #             self.timestamp = timestamp
    #             self.time_source = "exif"

    #         return
    #     else:
    #         raise AttributeError
    except AttributeError:
        pass
        # TODO exif not working always, use Video creation time function as well before default one
    except Exception as e:
        # print(f"thats new {e}")
        pass
