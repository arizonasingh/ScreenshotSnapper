"""
Author: Anmol Singh
GitHub: https://github.com/arizonasingh/ScreenshotSnapper
Purpose: To automate the process of capturing full web page screenshots in multiple viewports (desktop, mobile, tablet)
Date Created: 12 Apr 2019
"""

from utils import create_webdriver, get_folder
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from PIL import Image
from pathlib import Path
import os
import sys
import time
import datetime
import math

DEVICE_OPTIONS = {"1": "desktop", "2": "mobile", "3": "tablet"}
FILE_TYPE_OPTIONS = {"1": ".pdf", "2": ".png"}

class ScreenshotCaptureCLI:
    def __init__(self, device_type):
        self.driver = create_webdriver(device_type)

    def fullpage_screenshot(self, url, folder, filetype):
        print(f"Taking screenshot of {url}")

        # remove the browser vertical right side scrollbar from the screenshot
        # should work in all pages but since it is Javascript, it's good practice to enter in a try/except
        try:
            self.driver.execute_script("document.body.style.overflow = 'hidden';")
        except:
            print("This page did not allow the vertical scrollbar to be removed from the screenshot")
            time.sleep(0.1)

        total_height = self.driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = self.driver.execute_script("return window.innerWidth")
        viewport_height = self.driver.execute_script("return window.innerHeight")
        scale = self.driver.execute_script("return window.devicePixelRatio")

        rectangles = []

        i = 0
        while i < total_height:
            viewport_top_height = i + viewport_height

            if viewport_top_height > total_height:
                i = total_height - viewport_height
                viewport_top_height = total_height

            rectangles.append((0, i, 0, viewport_top_height))
            i = i + viewport_height

        stitched_image = Image.new('RGB', (int(viewport_width * scale), int(total_height * scale)))

        for j, rectangle in enumerate(rectangles):
            self.driver.execute_script(f"window.scrollTo({0}, {rectangle[1]})")
            time.sleep(0.2)

            tmp_img_name = f"section_{j}.png"
            self.driver.get_screenshot_as_file(tmp_img_name)
            screenshot = Image.open(tmp_img_name)

            self.remove_sticky_navs()

            if (j + 1) * viewport_height > total_height:
                offset = (0, int((total_height - viewport_height) * scale))
            else:
                offset = (0, int(j * viewport_height * scale - math.floor(j / 2.0)))

            stitched_image.paste(screenshot, offset)
            # not all below are valid URL characters but if ever functionality changed from URL to something else as the
            os.remove(tmp_img_name)

        # files have naming restrictions so saving file as the name of the URL (the below list covers filename forbidden
        # characters). Not all below are valid URL characters but if ever functionality changed from URL to something else
        # as the filename, the below will cover all restrictions. The file name can be changed below or additional
        # restrictions handled
        filename = url.replace("://", "_")
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

        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("  %Y-%m-%d %H_%M_%S")

        image_path = Path.joinpath(folder, filename + filetype)
        try:
            stitched_image.save(image_path)
        except:
            filename_excessive_length = True
            while filename_excessive_length:
                filename = filename[:-1]  # keep removing last character from filename until length is short enough to be
                # saved
                if os.path.exists(image_path):
                    filename = filename[:-21] + timestamp  # if by shortening filename the name already exists in the
                    # directory, add a timestamp to differentiate (remove same number of characters as the timestamp from
                    # filename)
                try:
                    stitched_image.save(image_path)
                    filename_excessive_length = False  # end loop if file is saved
                except:
                    filename = filename[:-1]  # not needed again since already at top but it will speed up the process a bit

        del stitched_image


    def btn_clicks(self):
        # parts of the page may need to be clicked based on your screenshot needs
        # add as many try/except clauses as you need to fit all your page needs
        # examples included below - since it's a try/catch, even if elements are not on the page, the program will not crash
        try:
            self.driver.find_element(By.XPATH,
                "//*[contains(text(),'Expand')]").click()  # for example if a T&C box needed to be expanded to capture
            # full text in screenshot
        except:
            time.sleep(0.1)

        self.driver.find_element(By.TAG_NAME,'body').send_keys(
            Keys.CONTROL + Keys.HOME)  # returning to top of page after clicking buttons


    def remove_sticky_navs(self):
        # many pages will have at least one sticky nav bar
        # unless they are removed or their position is set, the nav bar will appear multiple times in the screenshot
        # add as many try/except clauses as you need to fit all your page needs
        # examples included below - since it's a try/catch, even if elements are not on the page, the program will not crash
        try:
            self.driver.execute_script(
                "$('.header-wrapper').remove();")  # nav bar can be removed or fixed into place (static or absolute work
            # in most cases for position property - try .attr('style','position: static !important'); instead of .remove(
            # );)
            time.sleep(0.1)  # header-wrapper is common bootstrap nav bar class name
        except:
            time.sleep(0.1)


    def single_url(self, folder, filetype):
        url = input("\nEnter the URL: ")

        while not url.startswith("https://"):
            url = input("\nInvalid URL! Please enter a URL that starts with \"https://\": ")

        self.driver.get(url)

        self.btn_clicks()
        self.fullpage_screenshot(url, folder, filetype)
        print("Done!")
        self.driver.quit()


    def multiple_urls(self, folder, filetype):
        url_file = input("\nPlease drag a \".txt\" file here containing all the URLs on a new line: ")

        while not (url_file.endswith(".txt")) or not os.path.exists(url_file):  # Can be adjusted based on your
            # requirements. Feeding in a CSV for very large lists is recommended
            url_file = input("\nThat is not a valid file. Please drag a \".txt\" file here: ")

        url_list = open(url_file).read().splitlines()
        wrong_urls = ""

        for URL in url_list:
            if not URL.startswith("https://"):
                wrong_urls += URL + "\n"

        if wrong_urls:
            print("The following do not start with \"https://\" and must be fixed:\n\n" + wrong_urls)
            sys.exit()

        for URL in url_list:
            self.driver.get(URL)
            self.btn_clicks()
            self.fullpage_screenshot(URL, folder, filetype)

        print("Done!")
        self.driver.quit()


def open_screenshots(folder):
    if sys.platform == "win32":
        os.startfile(folder)
    elif sys.platform == "darwin":
        os.system('open "%s"' % folder)
    elif sys.platform == "linux":
        os.system('xdg-open "%s"' % folder)

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

    Please select an option ([1]/[2]/[3]): """, ("1", "2", "3"))

    if option == "3":
        print("Terminating Program")
        sys.exit()
    else:
        screenshotCapture = ScreenshotCaptureCLI(device)
        screenshot_dir = get_folder(device)

        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        if option == "1":
            screenshotCapture.single_url(screenshot_dir, file_extension)
        elif option == "2":
            screenshotCapture.multiple_urls(screenshot_dir, file_extension)

        # after all screenshots taken, open the folder containing the screenshots
        open_screenshots(screenshot_dir)
