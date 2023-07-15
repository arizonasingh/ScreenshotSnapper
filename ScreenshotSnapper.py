"""
Author: Anmol Singh
GitHub: https://github.com/arizonasingh/ScreenshotSnapper
Purpose: To automate the process of capturing full web page screenshots in multiple viewports (desktop, mobile, tablet)
Date Created: 12 Apr 2019
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from pathlib import Path
import os
import sys
import time
import datetime
import math

def build_driver(device):
    os.environ['WDM_LOCAL'] = '1'

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
    chrome_options.add_argument("log-level=3") # 0 = ALL, 1 = INFO, 2 = ERROR, 3 = FATAL
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # I am re-sizing the browser window to meet specific device type dimensions
    if device == "D":
        desktop = {"width": 1920,
                   "height": 1080}  # Should match the screen resolution size for a fully expanded browser
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        time.sleep(0.5)  # add a wait to allow driver to fully initialize
        driver.set_window_size(desktop['width'], desktop["height"])
        time.sleep(0.5)  # add a wait to allow window to fully re-size
    if device == "M":
        mobile = {"width": 375, "height": 812}  # iPhonde X dimensions; can be changed to meet your device configurations
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        time.sleep(0.5)  # add a wait to allow driver to fully initialize
        driver.set_window_size(mobile['width'], mobile["height"])
        time.sleep(0.5)  # add a wait to allow window to fully re-size
    if device == "T":
        tablet = {"width": 768, "height": 1024}  # iPad / iPad2 / iPad Mini dimensions; can be changed to meet your
        # device configurations
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        time.sleep(0.5)  # add a wait to allow driver to fully initialize
        driver.set_window_size(tablet['width'], tablet["height"])
        time.sleep(0.5)  # add a wait to allow window to fully re-size

    return driver

def fullpage_screenshot(driver, url, folder, filetype):
    print(f"Taking screenshot of {url}")

    # remove the browser vertical right side scrollbar from the screenshot
    # should work in all pages but since it is Javascript, it's good practice to enter in a try/except
    try:
        driver.execute_script("document.body.style.overflow = 'hidden';")
    except:
        print("This page did not allow the vertical scrollbar to be removed from the screenshot")
        time.sleep(0.1)

    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return window.innerWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
    scale = driver.execute_script("return window.devicePixelRatio")

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
        driver.execute_script(f"window.scrollTo({0}, {rectangle[1]})")
        time.sleep(0.2)

        tmp_img_name = f"section_{j}.png"
        driver.get_screenshot_as_file(tmp_img_name)
        screenshot = Image.open(tmp_img_name)

        remove_sticky_navs(driver)

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


def btn_clicks(driver):
    # parts of the page may need to be clicked based on your screenshot needs
    # add as many try/except clauses as you need to fit all your page needs
    # examples included below - since it's a try/catch, even if elements are not on the page, the program will not crash
    try:
        driver.find_element(By.XPATH,
            "//*[contains(text(),'Expand')]").click()  # for example if a T&C box needed to be expanded to capture
        # full text in screenshot
    except:
        time.sleep(0.1)

    driver.find_element(By.TAG_NAME,'body').send_keys(
        Keys.CONTROL + Keys.HOME)  # returning to top of page after clicking buttons


def remove_sticky_navs(driver):
    # many pages will have at least one sticky nav bar
    # unless they are removed or their position is set, the nav bar will appear multiple times in the screenshot
    # add as many try/except clauses as you need to fit all your page needs
    # examples included below - since it's a try/catch, even if elements are not on the page, the program will not crash
    try:
        driver.execute_script(
            "$('.header-wrapper').remove();")  # nav bar can be removed or fixed into place (static or absolute work
        # in most cases for position property - try .attr('style','position: static !important'); instead of .remove(
        # );)
        time.sleep(0.1)  # header-wrapper is common bootstrap nav bar class name
    except:
        time.sleep(0.1)


def single_url(device, folder, filetype):
    url = input("\nEnter the URL: ")

    while not url.startswith("https://"):
        url = input("\nInvalid URL! Please enter a URL that starts with \"https://\": ")

    driver = build_driver(device)
    driver.get(url)

    btn_clicks(driver)
    fullpage_screenshot(driver, url, folder, filetype)
    print("Done!")
    driver.quit()


def multiple_urls(device, folder, filetype):
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

    driver = build_driver(device)
    for URL in url_list:
        driver.get(URL)
        btn_clicks(driver)
        fullpage_screenshot(driver, URL, folder, filetype)

    print("Done!")
    driver.quit()

def open_screenshots(folder):
    if sys.platform == "win32":
        os.startfile(folder)
    elif sys.platform == "darwin":
        os.system('open "%s"' % folder)
    elif sys.platform == "linux":
        os.system('xdg-open "%s"' % folder)

if __name__ == '__main__':
    device = input("Please select a device ([D]esktop | [M]obile | [T]ablet): ")

    while device not in ({"D", "M", "T"}):
        print("\nNot a valid device")
        device = input("\nPlease select a device type ([D]/[M]/[T]): ")

    if device == "D":
        folder = Path("Screenshots/Desktop")
    if device == "M":
        folder = Path("Screenshots/Mobile")
    if device == "T":
        folder = Path("Screenshots/Tablet")

    if not os.path.exists(folder):
        os.makedirs(folder)

    filetype = input("\nSave image as ([1]PDF | [2]PNG): ")  # can be changed to meet your requirements

    while filetype not in ("1", "2"):
        print("\nNot a valid file type option")
        filetype = input("\nPlease select a file type option ([1]/[2]): ")

    if filetype == "1":
        filetype = ".pdf"  # change based on your requirements
    elif filetype == "2":
        filetype = ".png"  # change based on your requirements

    print("\n***NOTE: All URLs must start with \"https://\" and for Mobile and Tablet screenshots to be captured "
          "properly, the web page must be responsive***")
    option = input("\n[1] Single URL \n[2] Multiple URLs \n[3] Close Program \n\nPlease select an option ([1]/[2]/["
                   "3]): ")

    while option not in ("1", "2", "3"):
        print("\nNot a valid option")
        option = input("\nPlease select an option ([1]/[2]/[3]): ")
    if option == "1":
        single_url(device, folder, filetype)
    elif option == "2":
        multiple_urls(device, folder, filetype)
    elif option == "3":
        sys.exit()

    # after all screenshots taken, open the folder containing the screenshots
    open_screenshots(folder)
