import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options


@pytest.fixture(scope="function")
def driver():
    options = UiAutomator2Options()

    options.platform_name = "Android"
    options.device_name = "Android Emulator"
    options.automation_name = "UiAutomator2"

    options.app_package = "com.example.android.notepad"
    options.app_activity = ".NotePadActivity"

    options.no_reset = True
    options.new_command_timeout = 300

    driver = webdriver.Remote(
        "http://127.0.0.1:4723",
        options=options
    )

    yield driver

    driver.quit()