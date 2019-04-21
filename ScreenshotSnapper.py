"""
Author(s): Anmol Singh
GitHub: https://github.com/arizonasingh/
Purpose: To automate the process of capturing full web page screenshots in multiple viewports (desktop, mobile, tablet)
Date Created: 12 Apr 2019
"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from PIL import Image
from numpy import loadtxt
import os, sys, time, ctypes, math, win32api, win32con, pywintypes

def build_driver(device):
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
    chrome_options.add_argument("log-level=3") # Determines which console logs should be shown. Set to 0 for all messages, 1 for INFO and above, 2 for ERROR and above, and 3 for FATAL
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.headless = True # Set to true to run the program in the background (multi-tasking on other tasks is possible). Set to false to see the program running (warning: browser will open on screen so multi-tasking is not recommended as it will most likely affect the screen capture)

    # j am re-sizing the browser window to meet specific device type dimensions
    # Mobile emulation is possible, but the way the screenshots are taken, the images are enlarged sections of page and don't stitch correctly
    # If someone wants to fix the scrolling and screenshot capture by using mobile emulation, uncomment and use the below configs
    # mobile_emulation = {"deviceName": "iPhone X"} # Can be any of Google Chrome's supported Emulated Devices
    # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    # driver = webdriver.Chrome(executable_path="Drivers\\Chromedriver\\chromedriver.exe", options=chrome_options, desired_capabilities=chrome_options.to_capabilities())
    # If someone can figure that out, please reach out to me via GitHub (link in documentation above) and push the changes into the branch so j can see and test
    if device is "D":
        desktop = {"width": 1920, "height": 1080} # Should match the screen resolution size for a fully expanded browser
        driver = webdriver.Chrome(executable_path="Drivers\\Chromedriver\\chromedriver.exe", options=chrome_options)
        time.sleep(0.5) # add a wait to allow driver to fully initialize
        driver.set_window_size(desktop['width'], desktop["height"])
        time.sleep(0.5) # add a wait to window to fully re-size
    if device is "M":
        mobile = {"width": 375, "height": 812} #iPhone X dimensions; can be changed to meet your device configurations
        driver = webdriver.Chrome(executable_path="Drivers\\Chromedriver\\chromedriver.exe", options=chrome_options)
        time.sleep(0.5) # add a wait to allow driver to fully initialize
        driver.set_window_size(mobile['width'], mobile["height"])
        time.sleep(0.5) # add a wait to window to fully re-size
    if device is "T":
        tablet = {"width": 768, "height": 1024} #iPad / iPad2 / iPad Mini dimensions; can be changed to meet your device configurations
        driver = webdriver.Chrome(executable_path="Drivers\\Chromedriver\\chromedriver.exe", options=chrome_options)
        time.sleep(0.5) # add a wait to allow driver to fully initialize
        driver.set_window_size(tablet['width'], tablet["height"])
        time.sleep(0.5) # add a wait to window to fully re-size

    return driver

def fullpage_screenshot(driver, url, device, folder, filetype):
    print(f"Taking screenshot of {url}")
    
    js = ("window.document.styleSheets[0].insertRule(" + "'::-webkit-scrollbar {display: none;}', " + "window.document.styleSheets[0].cssRules.length);")
    driver.execute_script(js)
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

    stitched_image = Image.new('RGB',(int(viewport_width * scale), int(total_height * scale)))
    
    for j, rectangle in enumerate(rectangles):
        driver.execute_script(f"window.scrollTo({0}, {rectangle[1]})")
        time.sleep(0.2)

        tmpImgName = f"section_{j}.png"
        driver.get_screenshot_as_file(tmpImgName)
        screenshot = Image.open(tmpImgName)

        remove_sticky_navs(driver)

        if (j + 1) * viewport_height > total_height:
            offset = (0, int((total_height - viewport_height) * scale))
        else:
            offset = (0, int(j * viewport_height * scale - math.floor(j / 2.0)))

        stitched_image.paste(screenshot, offset)

        del screenshot
        os.remove(tmpImgName)

    # files have naming restrictions
    # saving file as name of url, thus handling common url characters that are restricted in file names
    # file name can be changed below or additional restrictions handled
    fileName = url.replace("://", "_")
    fileName = fileName.replace("/", "_")
    fileName = fileName.replace("?", "_")
    stitched_image.save(folder+fileName+filetype)
    del stitched_image

def btn_clicks(driver):
    # parts of the page may need to be clicked based on your screenshot needs
    # add as many try/except clauses as you need to fit all your page needs
    # examples included below - since it's a try/catch, even if elements are not on the page, the program will not crash
    try:
        BoxExpand = (driver.find_element_by_xpath("//*[contains(text(),'Expand')]")).click()
    except:
        time.sleep(0.1)
    
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME) # returning to top of page after clicking buttons

def remove_sticky_navs(driver):
    # many pages will have at least one sticky nav bar
    # unless they are removed or their position is set, the nav bar will appear multiple times in the screenshot
    # add as many try/except clauses as you need to fit all your page needs
    # examples included below - since it's a try/catch, even if elements are not on the page, the program will not crash
    try:
        driver.execute_script("$('.header-wrapper').remove();") # nav bar can be removed or fixed into place (static or absolute work in most cases for position property - try .attr('style','position: static !important'); instead of .remove();)
        time.sleep(0.1)
    except:
        time.sleep(0.1)

def single_url(device, folder, filetype):
    url = input("\nEnter the URL: ")

    while not url.startswith("https://"):
        url = input("\nInvalid URL! Please enter a URL that starts with \"https://\": ")
    
    driver = build_driver(device)
    driver.get(url)

    btn_clicks(driver)
    fullpage_screenshot(driver, url, device, folder, filetype)
    print("Done!")
    driver.quit()

def multiple_urls(device, folder, filetype):
    urlFile = input("\nPlease drag a \".txt\" file here containing all the URLs on a new line: ")
    
    while not urlFile.endswith(".txt"): # Can be adjusted based on your requirements. Feeding in a CSV for very large lists is recommended
        urlFile = input("\nThat is not a valid file. Please drag a \".txt\" file here: ")
    
    urlList = loadtxt(urlFile, dtype=str, comments="#", delimiter="\n", unpack=False)

    wrongURLs = ""

    for url in urlList:
        if not url.startswith("https://"):
            wrongURLs += url + "\n"
    
    if wrongURLs:
        win32api.ChangeDisplaySettings(None, 0)
        time.sleep(1.0) # add a wait to allow all elements on screen to adjust to new screen resolution
        ctypes.windll.user32.MessageBoxW(0, "The following do not start with \"https://\" and must be fixed:\n\n" + wrongURLs, "Invalid URL Error!", 0)
        sys.exit()
    
    driver = build_driver(device)
    for url in urlList:
        driver.get(url)
        btn_clicks(driver)
        fullpage_screenshot(driver, url, device, folder, filetype)
    
    print("Done!")
    driver.quit()

def screen_resolution(width, height):
    devmode = pywintypes.DEVMODEType()
    # adjust as necessary based on screen size
    devmode.PelsWidth = width
    devmode.PelsHeight = height
    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
    win32api.ChangeDisplaySettings(devmode, 0)
    time.sleep(3.0) # add a wait to allow all elements on screen to adjust to new screen resolution

if __name__ == '__main__':
    screen_resolution(1920, 1080) # Depending on computer monitor size, resolution may need to be adjusted

    device = input("Please select a device ([D]esktop | [M]obile | [T]ablet): ")

    while device not in ("D","M","T"):
        print("\nNot a valid device")
        device = input("\nPlease select a device type ([D]/[M]/[T]): ")
    
    if device is "D":
        folder = "Screenshots\\Desktop\\"
    if device is "M":
        folder = "Screenshots\\Mobile\\"
    if device is "T":
        folder = "Screenshots\\Tablet\\"

    if not os.path.exists(folder):
        os.makedirs(folder)

    filetype = input("\nSave image as ([1]PDF | [2]PNG): ") # can be changed to meet your requirements

    while filetype not in ("1","2"):
        print("\nNot a valid filetype option")
        filetype = input("\nPlease select a filetype option ([1]/[2]): ")

    if filetype is "1":
        filetype = ".pdf" # change based on your requirements
    elif filetype is "2":
        filetype = ".png" # change based on your requirements

    print("\n***NOTE: All URLs must start with \"https://\" and for Mobile and Tablet screenshots to be captured properly, the webpage must be responive***") #If mobile emulation works (see note in build_driver(device) method above), then the note about mobile and tablet can be removed
    option = input("\n[1] Single URL \n[2] Multiple URLs \n[3] Close Program and Restore Screen Resolution \n\nPlease select an option ([1]/[2]/[3]): ")

    while option not in ("1","2","3"):
        print("\nNot a valid option")
        option = input("\nPlease select an option ([1]/[2]/[3]): ")
    if option is "1":
        single_url(device, folder, filetype)
    elif option is "2":
        multiple_urls(device, folder, filetype)
    elif option is "3":
        win32api.ChangeDisplaySettings(None, 0)
        sys.exit()

    # after all screenshots taken, restore the screen resolution and open the folder
    win32api.ChangeDisplaySettings(None, 0)
    time.sleep(1.0) # add a wait to allow all elements on screen to adjust to new screen resolution
    os.startfile(folder)