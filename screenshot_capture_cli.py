"""
Author: Anmol Singh
GitHub: https://github.com/arizonasingh/ScreenshotSnapper
Purpose: To automate the process of capturing full web page screenshots in multiple viewports (desktop, mobile, tablet)
Date Created: 12 Apr 2019
"""

import os
import sys
from pathlib import Path

from screenshot_utils import click_buttons, remove_scrollbar, stitch_fullpage_screenshot, save_screenshot
from utils import create_webdriver, get_folder, open_screenshots, rename_file

DEVICE_OPTIONS = {"1": "desktop", "2": "mobile", "3": "tablet"}
FILE_TYPE_OPTIONS = {"1": ".pdf", "2": ".png"}
PROGRAM_OPTIONS = {"1": "Single", "2": "Multiple", "3": "Terminate"}

class ScreenshotCaptureCLI:
    def __init__(self, device_type):
        self.driver = create_webdriver(device_type)

    def fullpage_screenshot(self, url, folder, filetype):
        print(f"Taking screenshot of {url}")

        click_buttons(self.driver)
        remove_scrollbar(self.driver)

        stitched_image = stitch_fullpage_screenshot(self.driver)
        filename = rename_file(url)
        image_path = Path.joinpath(folder, filename + filetype)

        save_screenshot(stitched_image, image_path, filename)

    def single_url(self, folder, filetype):
        url = input("\nEnter the URL: ")

        while not url.startswith("https://"):
            url = input("\nInvalid URL! Please enter a URL that starts with \"https://\": ")

        self.driver.get(url)

        self.fullpage_screenshot(url, folder, filetype)
        print("Done!")
        self.driver.quit()

    def multiple_urls(self, folder, filetype):
        url_file = input("\nPlease drag a \".txt\" file here containing all the URLs on a new line: ")

        while not url_file.endswith(".txt") or not os.path.exists(url_file):
            url_file = input("\nThat is not a valid file. Please drag a \".txt\" file here: ")

        with open(url_file) as file:
            url_list = file.read().splitlines()

        wrong_urls = [url for url in url_list if not url.startswith("https://")]

        if wrong_urls:
            print("The following do not start with \"https://\" and must be fixed:\n")
            print("\n".join(wrong_urls))
            sys.exit()

        for url in url_list:
            self.driver.get(url)
            self.fullpage_screenshot(url, folder, filetype)

        print("Done!")
        self.driver.quit()

def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).strip()
        if user_input in valid_options:
            return user_input
        print("\nNot a valid option")

if __name__ == '__main__':
    device = get_valid_input("Please select a device ([1] Desktop | [2] Mobile | [3] Tablet): ", DEVICE_OPTIONS.keys())
    device = DEVICE_OPTIONS[device] # convert option to value

    file_extension = get_valid_input("\nSave image as ([1] PDF | [2] PNG): ", FILE_TYPE_OPTIONS.keys())
    file_extension = FILE_TYPE_OPTIONS[file_extension] # convert option to value

    print("""
    ***NOTE: All URLs must start with "https://" and for Mobile and Tablet screenshots to be captured properly,
    the web page must be responsive***"""
          )
    option = get_valid_input("""
    [1] Single URL
    [2] Multiple URLs
    [3] Close Program

    Please select an option ([1]/[2]/[3]): """, PROGRAM_OPTIONS.keys())
    option = PROGRAM_OPTIONS[option]

    if option == "Terminate":
        print("\nTerminating Program")
        sys.exit()
    else:
        screenshotCapture = ScreenshotCaptureCLI(device)
        screenshot_dir = get_folder(device)

        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        if option == "Single":
            screenshotCapture.single_url(screenshot_dir, file_extension)
        elif option == "Multiple":
            screenshotCapture.multiple_urls(screenshot_dir, file_extension)

        # after all screenshots taken, open the folder containing the screenshots
        open_screenshots(screenshot_dir)
