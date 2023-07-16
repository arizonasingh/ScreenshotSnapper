"""
Author: Anmol Singh
GitHub: https://github.com/arizonasingh/ScreenshotSnapper
Purpose: To store common functionality into a single file that can be shared with cli and gui programs
Date Created: 15 July 2023
"""
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import SCREEN_SIZES, FOLDER_DIRECTORIES


def create_webdriver(device_type):
    os.environ['WDM_LOCAL'] = '1'

    width, height = SCREEN_SIZES[device_type]

    arguments_list = [
        "test-type",
        "no-sandbox",
        "disable-extensions",
        "start-maximized",
        "--js-flags=--expose-gc",
        "disable-plugins",
        "--disable-popup-blocking",
        "--disable-default-apps",
        "test-type=browser",
        "disable-infobars",
        "--headless",
        "log-level=3",
    ]

    chrome_options = webdriver.ChromeOptions()
    for argument in arguments_list:
        chrome_options.add_argument(argument)

    chrome_options.add_argument(f"--window-size={width},{height}")
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    return driver

def get_folder(device_type):
    return Path(FOLDER_DIRECTORIES[device_type])

def open_screenshots(folder):
    try:
        if sys.platform == "win32":
            subprocess.run(['start', '', folder], check=True, shell=True)
        elif sys.platform == "darwin":
            subprocess.run(['open', folder], check=True)
        elif sys.platform == "linux":
            subprocess.run(['xdg-open', folder], check=True)
    except subprocess.CalledProcessError:
        print("Failed to open the folder.")

def rename_file(filename):
    characters_to_replace = ["://", "\\", "/", ":", "*", "?", "\"", "<", ">", "|", ".", "=", "%"]

    for char in characters_to_replace:
        filename = filename.replace(char, "_")

    return filename

def is_valid_url(url):
    parsed_url = urlparse(url)

    if parsed_url.netloc:
        return True

    return False
