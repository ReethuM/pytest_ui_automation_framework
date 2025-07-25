import os
import time


def take_screenshot(driver, test_name):
    folder = "screenshots"
    os.makedirs(folder, exist_ok=True)

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{test_name}_{timestamp}.png"
    path = os.path.join(folder, filename)

    driver.save_screenshot(path)
    print(f"Screenshot saved to: {path}")
    return path
