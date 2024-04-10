# File Sorter

This python script scans through provided files, categorizes, sorts, copies
and removes duplicates (duplicate operations working only for images).

## Prerequisities

Install third party modules:

```python
python3 -m pip install -r requirements.txt
```

## Usage

To run, call:

```python
python3 main.py
```

two windows will apear, first one asking for destination, latter one for the target
directory.

To change categories, edit `sorter/categories.py` file.

To change duplicate image behavior, call (installed) `find_dups -h` or
see [their API](https://github.com/lene/DuplicateImages) and edit `sys.argv`
in `main.py`.
