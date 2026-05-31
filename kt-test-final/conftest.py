import pytest
import allure
from selenium import webdriver
from allure_commons.types import AttachmentType


def pytest_addoption(parser):
    """Добавляем пользовательские опции командной строки"""
    parser.addoption("--browser", action="store", default="chrome", help="Browser: chrome or firefox")
    parser.addoption("--grid", action="store_true", default=False, help="Use Selenium Grid")


@pytest.fixture(scope="function")
def driver(request):
    """Фикстура для создания WebDriver (локально или через Grid)"""
    use_grid = request.config.getoption("--grid")
    browser = request.config.getoption("--browser")
    
    if use_grid:
        # Запуск через Selenium Grid (standalone)
        if browser == "chrome":
            options = webdriver.ChromeOptions()
        else:
            options = webdriver.FirefoxOptions()
        driver = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            options=options
        )
    else:
        # Локальный запуск
        if browser == "chrome":
            driver = webdriver.Chrome()
        else:
            driver = webdriver.Firefox()
    
    driver.maximize_window()
    yield driver
    
    # Проверяем, упал ли тест (с проверкой существования атрибута)
    if hasattr(request.node, 'rep_call') and request.node.rep_call and request.node.rep_call.failed:
        allure.attach(
            driver.get_screenshot_as_png(), 
            name="screenshot_on_failure", 
            attachment_type=allure.attachment_type.PNG
        )
    
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для обработки отчета о выполнении теста.
    Добавляет время выполнения теста в Allure-отчет.
    """
    outcome = yield
    report = outcome.get_result()
    
    # Сохраняем отчет в item для доступа из фикстуры
    setattr(item, "rep_" + report.when, report)
    
    # Добавляем время выполнения только для этапа вызова теста (call)
    if report.when == "call":
        duration = report.duration
        allure.attach(
            f"Duration: {duration:.2f} seconds", 
            name="Execution Time", 
            attachment_type=allure.attachment_type.TEXT
        )