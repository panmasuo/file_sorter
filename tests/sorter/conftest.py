from datetime import datetime
from pathlib import Path


TEST_VIDEO_FILES = {
    "video_001": {
        "path": Path("tests\\data\\test-video-001.mp4"),
        "name": "2024-08-17_1723917771000000000.mp4",
        "datetime": datetime(year=2024, month=8, day=17,
                             hour=20, minute=2, second=51),
    },
    "video_002": {
        "path": Path("tests\\data\\test-video-002.mp4"),
        "name": "2024-08-20_1724148151000000000.mp4",
        "datetime": datetime(year=2024, month=8, day=20,
                             hour=12, minute=2, second=31),
    },
    "video_003": {
        "path": Path("tests\\data\\test-video-003.mp4"),
        "name": "2024-11-04_1730754744000000000.mp4",
        "datetime": datetime(year=2024, month=11, day=4,
                             hour=22, minute=12, second=24),
    },
}
