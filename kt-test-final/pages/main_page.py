import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class MainPage(BasePage):
    
    def open(self, url: str = "https://ege.sdamgia.ru/"):
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(2)
        return self
    
    def get_page_title(self) -> str:
        return self.driver.title
    
    def get_current_url(self) -> str:
        return self.driver.current_url
    
    def take_screenshot_and_attach(self, name: str):
        screenshot = self.driver.get_screenshot_as_png()
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        return screenshot
    
    def find_and_click(self, selector: str, selector_type: str = "css", timeout: int = 10):
        """Универсальный метод поиска и клика"""
        by = By.CSS_SELECTOR if selector_type == "css" else By.XPATH
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, selector))
        )
        element.click()
        return element
    
    def find_and_send_keys(self, selector: str, text: str, selector_type: str = "css"):
        """Универсальный метод ввода текста"""
        by = By.CSS_SELECTOR if selector_type == "css" else By.XPATH
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, selector))
        )
        element.clear()
        element.send_keys(text)
        return element