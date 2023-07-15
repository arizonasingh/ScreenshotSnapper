import datetime
import math
import os
import time

from PIL import Image

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


def remove_sticky_navs(driver):
    # many pages will have at least one sticky nav bar
    # unless they are removed or their position is set, the nav bar will appear multiple times in the screenshot
    # add as many try/except clauses as you need to fit all your page needs
    # examples included below - since it's a try/catch, even if elements are not on the page, the program will not crash
    try:
        # nav bar can be removed or fixed into place (static or absolute work
        # in most cases for position property - try .attr('style','position: static !important'); instead of .remove(
        # );)
        driver.execute_script(
            "$('.header-wrapper').remove();")  # header-wrapper is common bootstrap nav bar class name
        time.sleep(0.1)
    except:
        time.sleep(0.1)

def click_buttons(driver):
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

def remove_scrollbar(driver):
    # remove the browser vertical right side scrollbar from the screenshot
    # should work in all pages but since it is Javascript, it's good practice to enter in a try/except
    try:
        driver.execute_script("document.body.style.overflow = 'hidden';")
    except:
        print("This page did not allow the vertical scrollbar to be removed from the screenshot")
        time.sleep(0.1)

def stitch_fullpage_screenshot(driver):
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

    return stitched_image

def save_screenshot(stitched_image, image_path, filename):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("  %Y-%m-%d %H_%M_%S")

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
