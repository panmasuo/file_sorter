import pytest
from datetime import datetime
from pathlib import Path

# TODO find picture that creates that error:
# D:\workspace\file_sorter\env\Lib\site-packages\exif\_image.py:171: RuntimeWarning: ASCII tag contains -1 fewer bytes than specified
#   retval = getattr(self, attribute)

TEST_IMAGE_FILES = {
    # image with "[err!] [/exif/content/exif[0]/value[27]/data[2]]"
    # Unable to create value: float division by zero
    "image_001": {
        "path": Path("tests/data/test-image-001.jpg"),
        "name": "2021-08-21_1629560464220000000.jpg",
        "datetime": datetime(year=2021, month=8, day=21,
                             hour=17, minute=41, second=4),
        "output": Path("tests/output/video/2021"),
    },
}

TEST_VIDEO_FILES = {
    # sanity check
    "video_001": {
        "path": Path("tests/data/test-video-001.mp4"),
        "name": "2024-08-17_1723917771000000000.mp4",
        "datetime": datetime(year=2024, month=8, day=17,
                             hour=20, minute=2, second=51),
        "output": Path("tests/output/video/2024"),
    },
    # not copied when app is running
    "video_002": {
        "path": Path("tests/data/test-video-002.mp4"),
        "name": "2021-07-23_1627038653000000000.mp4",
        "datetime": datetime(year=2021, month=7, day=23,
                             hour=13, minute=10, second=53),
        "output": Path("tests/output/video/2021"),
    },
}


@pytest.fixture(scope="session", autouse=True)
def handle_output_directory():
    """Fixture for creating and deleting all created output files after
    testing session.
    """
    output_dir = Path("tests/output")
    output_dir.mkdir()

    yield

    output_dir = Path("tests/output")
    if not output_dir.exists():
        return

    _ = [item.unlink() for item in output_dir.iterdir() if item.is_file()]
