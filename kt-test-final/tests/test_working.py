import allure
import time
import pytest
from selenium.webdriver.common.by import By
from pages.main_page import MainPage

@allure.epic("Портал подготовки к ЕГЭ")
@allure.feature("Базовые проверки")
@allure.story("Открытие страниц")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "critical")
def test_main_page_opens(driver):
    """Тест: главная страница открывается"""
    with allure.step("Открываем главную страницу"):
        page = MainPage(driver).open("https://ege.sdamgia.ru/")
        time.sleep(2)
    
    with allure.step("Проверяем заголовок страницы"):
        title = page.get_page_title()
        allure.attach(title, name="Page Title", attachment_type=allure.attachment_type.TEXT)
    
    with allure.step("Проверяем URL"):
        url = page.get_current_url()
        allure.attach(url, name="Page URL", attachment_type=allure.attachment_type.TEXT)
    
    assert "sdamgia" in url or "ege" in url.lower()


@allure.epic("Портал подготовки к ЕГЭ")
@allure.feature("Скриншоты")
@allure.story("Визуальная фиксация")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("visual")
def test_screenshot_main_page(driver):
    """Тест: создание скриншота главной страницы"""
    with allure.step("Открываем главную страницу"):
        page = MainPage(driver).open("https://ege.sdamgia.ru/")
        time.sleep(2)
    
    with allure.step("Делаем скриншот"):
        screenshot = page.take_screenshot_and_attach("main_page_screenshot")
    
    with allure.step("Проверяем что скриншот создан"):
        assert screenshot is not None


@allure.epic("Портал подготовки к ЕГЭ")
@allure.feature("Поиск элементов")
@allure.story("Анализ страницы")
@allure.severity(allure.severity_level.MINOR)
def test_find_all_links(driver):
    """Тест: поиск всех ссылок на главной странице"""
    with allure.step("Открываем главную страницу"):
        page = MainPage(driver).open("https://ege.sdamgia.ru/")
        time.sleep(2)
    
    with allure.step("Ищем все ссылки на странице"):
        links = driver.find_elements(By.TAG_NAME, "a")
        link_count = len(links)
    
    with allure.step("Логируем результат"):
        allure.attach(f"Найдено ссылок: {link_count}", name="Links count", attachment_type=allure.attachment_type.TEXT)
        for i, link in enumerate(links[:10]):
            if link.text:
                allure.attach(link.text, name=f"Link {i+1}", attachment_type=allure.attachment_type.TEXT)
    
    assert link_count > 0