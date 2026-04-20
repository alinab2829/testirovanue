from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

GRID_URL = "http://localhost:4444"

EVENT_NAME = "ленинград"


# =========================
# DRIVER GRID
# =========================
def create_driver(browser):
    if browser == "chrome":
        options = Options()
        options.set_capability("browserName", "chrome")

    elif browser == "firefox":
        options = FFOptions()
        options.set_capability("browserName", "firefox")

    return webdriver.Remote(
        command_executor=GRID_URL,
        options=options
    )


# =========================
# 1. ПОИСК
# =========================
def search_event(driver, browser):
    wait = WebDriverWait(driver, 20)

    driver.get("https://afisha.yandex.ru/vladivostok")

    search = wait.until(
        EC.element_to_be_clickable((By.TAG_NAME, "input"))
    )

    search.send_keys(EVENT_NAME)
    search.send_keys(Keys.ENTER)

    print(f"SEARCH DONE ({browser})")


# =========================
# 2. ОТКРЫТЬ МЕРОПРИЯТИЕ
# =========================
def open_event(driver, browser):
    wait = WebDriverWait(driver, 20)

    time.sleep(3)

    event = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(@href,'event') or contains(.,'Ленинград') or contains(.,'концерт')]"
        ))
    )

    driver.execute_script("arguments[0].click();", event)

    print(f"EVENT OPENED ({browser})")


# =========================
# 3. НАЖАТЬ "КУПИТЬ БИЛЕТ"
# =========================
def buy_ticket(driver, browser):
    wait = WebDriverWait(driver, 20)

    try:
        btn = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(.,'Купить') or contains(.,'Билеты')]"
            ))
        )

        driver.execute_script("arguments[0].click();", btn)

        print(f"BUY CLICKED ({browser})")

    except Exception:
        print(f"BUY BUTTON NOT FOUND ({browser})")


# =========================
# 4. ВОЗВРАТ НАЗАД
# =========================
def go_back(driver, browser):
    time.sleep(2)
    driver.back()
    print(f"BACK TO LIST ({browser})")


# =========================
# RUN FLOW
# =========================
def run(browser):
    driver = create_driver(browser)

    try:
        search_event(driver, browser)
        open_event(driver, browser)
        buy_ticket(driver, browser)
        go_back(driver, browser)

    except Exception as e:
        print(f"ERROR ({browser}): {e}")

    finally:
        driver.quit()
        print(f"BROWSER CLOSED ({browser})")


# =========================
# MAIN
# =========================
if __name__ == "__main__":

    for b in ["chrome", "firefox"]:
        print("\n" + "=" * 60)
        print(f"RUN {b.upper()}")
        print("=" * 60)

        run(b)

    print("\nDONE")
