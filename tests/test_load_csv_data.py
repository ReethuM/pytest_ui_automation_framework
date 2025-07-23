import csv
import pytest
from selenium.webdriver.common.by import By


def load_csv_data(filename):
    data = []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append((row['username'], row['password']))
    return data


@pytest.mark.parametrize("username, password", load_csv_data("test_data\\test_data.csv"))
def test_csv_data(driver, username, password):
    driver.get("https://practicetestautomation.com/practice-test-login/")
    driver.find_element("id", "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@id='submit']").click()
