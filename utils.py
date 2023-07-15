from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
import sys, os

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

def open_screenshots(folder):
    if sys.platform == "win32":
        os.startfile(folder)
    elif sys.platform == "darwin":
        os.system('open "%s"' % folder)
    elif sys.platform == "linux":
        os.system('xdg-open "%s"' % folder)

def rename_file(filename):
    # files have naming restrictions so saving file as the name of the URL (the below list covers filename forbidden
    # characters). Not all below are valid URL characters but if ever functionality changed from URL to something else
    # as the filename, the below will cover all restrictions. The file name can be changed below or additional
    # restrictions handled
    filename = filename.replace("://", "_")
    filename = filename.replace("\\", "_")
    filename = filename.replace("/", "_")
    filename = filename.replace(":", "_")
    filename = filename.replace("*", "_")
    filename = filename.replace("?", "_")
    filename = filename.replace("\"", "_")
    filename = filename.replace("<", "_")
    filename = filename.replace(">", "_")
    filename = filename.replace("|", "_")
    filename = filename.replace(".", "_")

    return filename