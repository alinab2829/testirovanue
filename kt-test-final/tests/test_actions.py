import allure
import time
from pages.main_page import MainPage

@allure.feature("Навигация по сайту")
def test_main_page_loads(driver):
    """Тест: главная страница загружается"""
    page = MainPage(driver).open()
    time.sleep(2)
    title = page.get_page_title()
    assert title is not None
    allure.attach(driver.get_screenshot_as_png(), name="main_page", attachment_type=allure.attachment_type.PNG)


@allure.feature("Скриншоты")
def test_catalog_opens(driver):
    """Тест: каталог открывается"""
    driver.get("https://ege.sdamgia.ru/problem")
    time.sleep(3)
    allure.attach(driver.get_screenshot_as_png(), name="catalog", attachment_type=allure.attachment_type.PNG)
    assert "problem" in driver.current_url


@allure.feature("Скриншоты")
def test_main_page_screenshot(driver):
    """Тест: скриншот главной страницы"""
    driver.get("https://ege.sdamgia.ru/")
    time.sleep(3)
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)
    assert screenshot is not None