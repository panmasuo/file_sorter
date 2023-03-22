from pathlib import Path
from tkinter.filedialog import askdirectory

DEFAULT_ASK_DIRECTORY_TITLE = "Please pick directory"


def get_directory(title: str = DEFAULT_ASK_DIRECTORY_TITLE) -> Path:
    dir = askdirectory(initialdir=".", title=title)

    if not dir:
        raise RuntimeError("Directory was root or was not picked")

    return Path(dir)
