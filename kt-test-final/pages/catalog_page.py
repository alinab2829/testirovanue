import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class CatalogPage(BasePage):
    
    def open(self):
        self.driver.get("https://ege.sdamgia.ru/problem")
        return self