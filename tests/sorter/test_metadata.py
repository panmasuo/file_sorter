import logging

import sorter.metadata as md
from conftest import TEST_IMAGE_FILES, TEST_VIDEO_FILES

# configure logging before anything else
logging.basicConfig(level=logging.DEBUG,
                    format="[%(levelname)s %(name)s:%(lineno)d] %(message)s")
log = logging.getLogger("test")

def test_if_valid_files_return_correct_name_datetime():
    """If video path is correct, extracted name and date should match
    defined values."""
    for _, value in TEST_VIDEO_FILES.items():
        name, date = md.create_name_and_date(value["path"])

        assert name == value["name"]
        assert date == value["datetime"]

    for _, value in TEST_IMAGE_FILES.items():
        name, date = md.create_name_and_date(value["path"])

        assert name == value["name"]
        assert date == value["datetime"]
