from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import os

from config import SCREEN_SIZES, FOLDER_DIRECTORIES


def create_webdriver(device_type):
    os.environ['WDM_LOCAL'] = '1'

    width, height = SCREEN_SIZES[device_type]

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("test-type")
    chrome_options.add_argument("no-sandbox")
    chrome_options.add_argument("disable-extensions")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--js-flags=--expose-gc")
    chrome_options.add_argument("disable-plugins")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("test-type=browser")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("log-level=3")  # 0 = ALL, 1 = INFO, 2 = ERROR, 3 = FATAL
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument(f"--window-size={width},{height}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    return driver

def get_folder(device_type):
    return Path(FOLDER_DIRECTORIES[device_type])
