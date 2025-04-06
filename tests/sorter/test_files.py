from pathlib import Path

from conftest import TEST_IMAGE_FILES
from sorter.files import FileType


def test_if_same_metadata_then_add_iterator():
    """Copies same file multiple times and checks if renaming was correctly
    applied.
    """
    photo = TEST_IMAGE_FILES["image_001"]
    NO_OF_COPIES = 3

    expected_names = [
        # replace last digit with i, e.g. abc_000.jpg, abc_001.jpg ...
        f"{photo['name'][:-5]}{i}{photo['name'][-4:]}"
        for i in range(NO_OF_COPIES)
    ]

    for i in range(NO_OF_COPIES):
        file = FileType(photo["path"])
        while not file.copy(Path("tests\\output\\")):
            file.rename_duplicate()

        assert Path(photo["output"] / expected_names[i]).exists
