from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def create_webdriver() -> Chrome:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = Chrome(options=chrome_options)

    return driver
