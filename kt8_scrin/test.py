import os
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageChops
import imagehash


BASELINE_DIR = "baselines"
DIFF_DIR = "diffs"

os.makedirs(BASELINE_DIR, exist_ok=True)
os.makedirs(DIFF_DIR, exist_ok=True)


@pytest.fixture
def browser():
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(options=opts)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()


def compare_images(img1_path, img2_path, diff_path):
    img1 = Image.open(img1_path).convert("RGB")
    img2 = Image.open(img2_path).convert("RGB")

    h1 = imagehash.phash(img1)
    h2 = imagehash.phash(img2)

    if (h1 - h2) > 5:
        diff = ImageChops.difference(img1, img2)
        diff.save(diff_path)
        return False

    return True


def test_docs_vs_community(browser):
    wait = WebDriverWait(browser, 15)

    docs_path = os.path.join(BASELINE_DIR, "docs.png")
    community_path = os.path.join(BASELINE_DIR, "community.png")
    diff_path = os.path.join(DIFF_DIR, "docs_vs_community_diff.png")


    browser.get("https://www.python.org/doc/")
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    browser.save_screenshot(docs_path)

  
    browser.get("https://www.python.org/doc/")
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    link = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/community/"]'))
    )
    link.click()

    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    browser.save_screenshot(community_path)

    assert compare_images(docs_path, community_path, diff_path), \
        f"Docs и Community отличаются: {diff_path}"
