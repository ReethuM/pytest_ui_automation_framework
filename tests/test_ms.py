import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def test_missing_element(driver):
    driver.get("https://practicetestautomation.com")

    with pytest.raises(NoSuchElementException) as exc:
        driver.find_element(By.ID,  "non_existing_element")
        # driver.find_element(By.ID,  "menu-item-20") --> this will fail the test as the exception was not raised bcz
        # the element is present

    # print(exc.value, exc.type, exc.tb)
    assert "no such element" in str(exc.value).lower()
