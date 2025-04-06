from sorter.categories import (
    FileCategories, FILE_IMAGE_SUFFIXES, get_file_category
)


class DummyPath:
    """Mocks Path class."""
    DUMMY_TEST_SUFFIX = ".test"

    # suffix is checked by categories module, set dummy one for tests
    suffix = DUMMY_TEST_SUFFIX


def test_if_suffix_in_rename_category_then_return_trash_category():
    """If suffix given in DummyPath object is not present in declared
    image or video suffixes, it is categorized as trash.
    """
    assert FileCategories.TRASH is get_file_category(DummyPath)


def test_if_suffix_in_rename_category_then_return_category():
    """If suffix given in DummyPath object is present in declared
    image suffixes, it is categorized as photo.
    """
    # add test suffix to allowed image suffixes
    FILE_IMAGE_SUFFIXES.add(DummyPath.DUMMY_TEST_SUFFIX)

    assert FileCategories.PHOTO is get_file_category(DummyPath)
