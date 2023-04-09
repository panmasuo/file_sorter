from pathlib import Path

import cv2

from sorter.categories import FileCategories


class Picker:
    def __init__(self):
        pass

    def _read_files(self, file: Path):
        category = file._file_class
        if category is FileCategories.PHOTO:
            read = cv2.imread
        elif category is FileCategories.VIDEO:
            read = cv2.VideoCapture
        else:
            return

        options = (read(f"{file._file}"), read(f"{file._dup_target}"))
        return options, category

    def _resize(self, options):
        if options[0].shape[0] != options[1].shape[0]:
            height = max(options[0].shape[0], options[1].shape[0])
            width1 = int(options[0].shape[1] * height / options[0].shape[0])
            width2 = int(options[1].shape[1] * height / options[1].shape[0])
            options = (cv2.resize(options[0], (width1, height)), cv2.resize(options[1], (width2, height)))

        concated = cv2.hconcat([options[0], options[1]])
        # Get the dimensions of the screen
        screen_width, screen_height = 1280, 720
        screen_ratio = screen_width / screen_height

        # Get the dimensions of the image
        img_height, img_width, _ = concated.shape
        img_ratio = img_width / img_height

        # Determine the scaling factor
        if img_ratio > screen_ratio:
            scale_factor = screen_width / img_width
        else:
            scale_factor = screen_height / img_height

        # Resize the image
        return cv2.resize(concated, None, fx=scale_factor, fy=scale_factor)

    def _get_screen(self, options, category):
        if category is FileCategories.PHOTO:
            return self._resize(options)
        elif category is FileCategories.VIDEO:
            # read only first frame
            ret1, frame1 = options[0].read()
            ret2, frame2 = options[1].read()

            options[0].release()
            options[1].release()

            if ret1 and ret2:
                return self._resize((frame1, frame2))

    def compare(self, file: Path):
        cv2.namedWindow("Picker", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Picker", 1280, 720)

        status = None
        # check for NULL
        options, category = self._read_files(file)
        screen = self._get_screen(options, category)
        while screen is not None:
            cv2.imshow("Picker", screen)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                status = "c"
                break
            elif key == ord('n'):
                status = "n"
                break

        cv2.destroyAllWindows()

        return status
