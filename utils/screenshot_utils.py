import os
import time
from glob import glob


class ScreenshotManager:
    MAX_SCREENSHOTS_PER_FOLDER = 5

    @staticmethod
    def take_screenshot(driver, test_name, status):

        date_str = time.strftime('%Y-%m-%d')
        time_str = time.strftime('%H-%M-%S')

        folder = os.path.abspath(os.path.join("screenshots", status, date_str))
        os.makedirs(folder, exist_ok=True)

        ScreenshotManager.delete_older_screenshots(folder)

        filename = f"{test_name}_{time_str}.png"
        file_path = os.path.join(folder, filename)

        driver.save_screenshot(file_path)
        return file_path

    @staticmethod
    def delete_older_screenshots(folder):
        screenshots = sorted(glob(os.path.join(folder, "*.png")),
                             key=os.path.getctime)

        if len(screenshots) >= ScreenshotManager.MAX_SCREENSHOTS_PER_FOLDER:
            to_delete = len(screenshots) - ScreenshotManager.MAX_SCREENSHOTS_PER_FOLDER
            for i in range(to_delete):
                os.remove(screenshots[i])
                print(f"Deleted older screenshot: {screenshots[i]}")
