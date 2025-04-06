import pytest
from datetime import datetime
from pathlib import Path


TEST_IMAGE_FILES = {
    # image with hachoir "[err!] [/exif/content/exif[0]/value[27]/data[2]]"
    # Unable to create value: float division by zero
    "image_001": {
        "path": Path("tests/media/test-image-001.jpg"),
        "name": "2021-08-21_1629560464220000000.jpg",
        "datetime": datetime(year=2021, month=8, day=21,
                             hour=17, minute=41, second=4),
        "output": Path("tests/output/video/2021"),
    },

    # image with exif error: env\Lib\site-packages\exif\_image.py:171:
    #   RuntimeWarning: ASCII tag contains -1 fewer bytes than specified
    #       retval = getattr(self, attribute)
    "image_002": {
        "path": Path("tests/media/test-image-002.jpg"),
        "name": "2016-05-21_1463817789000000000.jpg",
        "datetime": datetime(year=2016, month=5, day=21,
                             hour=10, minute=3, second=9),
        "output": Path("tests/output/photo/2016"),
    },
}

TEST_VIDEO_FILES = {
    # sanity check
    "video_001": {
        "path": Path("tests/media/test-video-001.mp4"),
        "name": "2024-08-17_1723917771000000000.mp4",
        "datetime": datetime(year=2024, month=8, day=17,
                             hour=20, minute=2, second=51),
        "output": Path("tests/output/video/2024"),
    },
}


@pytest.fixture(scope="session", autouse=True)
def handle_output_directory():
    """Fixture for creating and deleting all created output files after
    testing session.
    """
    output_dir = Path("tests/output")
    output_dir.mkdir(exist_ok=True)

    yield

    output_dir = Path("tests/output")
    if not output_dir.exists():
        return

    # remove files
    for item in output_dir.rglob("*"):
        if item.is_file():
            item.unlink()

    # remove directories
    for item in sorted(output_dir.rglob("*"), key=lambda obj: -len(obj.parts)):
        # if is dir and does not contain anything
        if item.is_dir() and not any(item.iterdir()):
            item.rmdir()
    else:
        output_dir.rmdir()
