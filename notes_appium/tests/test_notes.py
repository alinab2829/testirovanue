from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_create_note(driver):
    wait = WebDriverWait(driver, 20)

    # 1. открыть создание заметки
    wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "com.example.android.notepad:id/fab_add")
        )
    ).click()

    # 2. ввод текста
    fields = wait.until(
        EC.presence_of_all_elements_located(
            (AppiumBy.CLASS_NAME, "android.widget.EditText")
        )
    )

    fields[0].send_keys("Test note")

    if len(fields) > 1:
        fields[1].send_keys("Hello Appium")

    # 3. 🔥 УМНОЕ СОХРАНЕНИЕ (НЕ back сразу)
    driver.press_keycode(4)  # Android BACK

    # 4. иногда нужно второй back (очень важно)
    try:
        wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ID, "com.example.android.notepad:id/fab_add")
            )
        )
    except:
        driver.press_keycode(4)

    # 5. теперь точно ждём главный экран
    fab = wait.until(
        EC.presence_of_element_located(
            (AppiumBy.ID, "com.example.android.notepad:id/fab_add")
        )
    )

    # 6. проверка заметки
    note = wait.until(
        EC.presence_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR,
             'new UiSelector().textContains("Test note")')
        )
    )

    assert note.is_displayed()