from pathlib import Path
from tkinter.filedialog import askdirectory

DEFAULT_ASK_DIRECTORY_TITLE = "Please pick directory"


def get_directory_path(title: str = DEFAULT_ASK_DIRECTORY_TITLE) -> Path:
    """Asks user for directory path and returns it.

    Args:
        title (str, optional): Dialog window title. Defaults
        to DEFAULT_ASK_DIRECTORY_TITLE.

    Raises:
        RuntimeError: In case where action was canceled by
        the user.

    Returns:
        Path: Path to the directory.
    """
    dir = askdirectory(initialdir=".", title=title)

    if not dir:
        raise RuntimeError("askdirectory dialog window was cancelled")

    return Path(dir)
