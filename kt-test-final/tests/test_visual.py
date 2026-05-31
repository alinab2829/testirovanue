import allure
import time
from pages.main_page import MainPage

@allure.feature("Визуальная проверка")
def test_visual_main_page(driver):
    """Визуальная проверка главной страницы"""
    page = MainPage(driver).open("https://ege.sdamgia.ru/")
    time.sleep(3)
    
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name="main_page_visual", attachment_type=allure.attachment_type.PNG)
    assert screenshot is not None


@allure.feature("Визуальная проверка")
def test_visual_catalog_page(driver):
    """Визуальная проверка страницы каталога"""
    driver.get("https://ege.sdamgia.ru/problem")
    time.sleep(3)
    
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name="catalog_visual", attachment_type=allure.attachment_type.PNG)
    assert screenshot is not None