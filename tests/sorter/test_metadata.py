import sorter.metadata as md
from conftest import TEST_VIDEO_FILES


def test_if_valid_video_return_correct_name_datetime():
    """If video path is correct, extracted name and date should match
    defined values."""
    for _, value in TEST_VIDEO_FILES.items():
        name, date = md.create_name_and_date(value["path"])

        print(name, date)

        assert name == value["name"]
        assert date == value["datetime"]
