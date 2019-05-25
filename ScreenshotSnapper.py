__version__ = "1.4.1"
"""
Author: Anmol Singh
GitHub: https://github.com/arizonasingh/
Purpose: To automate the process of capturing full web page screenshots in multiple viewports (desktop, mobile, tablet)
Date Created: 12 Apr 2019
"""

### IMPORTS BEGIN HERE ###
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from PIL import Image
from numpy import loadtxt
import os, sys, time, datetime, ctypes, math
### IMPORTS END HERE ###

### SCREENSHOT CAPTURE BEGINS HERE ###
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

    # I am re-sizing the browser window to meet specific device type dimensions
    # Mobile emulation is possible, but the way the screenshots are taken, the images are enlarged sections of page and don't stitch correctly
    # If someone wants to fix the scrolling and screenshot capture by using mobile emulation, uncomment and use the below configs
    # mobile_emulation = {"deviceName": "iPhone X"} # Can be any of Google Chrome's supported Emulated Devices
    # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    # driver = webdriver.Chrome(executable_path="Drivers\\Chromedriver\\chromedriver.exe", options=chrome_options, desired_capabilities=chrome_options.to_capabilities())
    # If someone can figure that out, please reach out to me via GitHub (link in documentation above) and push the changes into the branch so j can see and test
    if device is "D":
        desktop = {"width": 1920, "height": 1080} # Should match the screen resolution size for a fully expanded browser
        try:
            driver = webdriver.Chrome(executable_path="Drivers\\Chromedriver\\chromedriver.exe", options=chrome_options)
        except:
            ctypes.windll.user32.MessageBoxW(0, "Program could not execute! Possible errors:\n\n1. Google Chrome v74 is not installed on your device\n2. Missing Chromedriver. Could not find \"Drivers/Chromedriver/Chromedriver.exe\" which is often the result of moving the application from the source location. To use outside its source location, \"copy\" or \"create a shortcut\" but do not move the original program from its source location unless all dependencies are moved along with it.", "Chromedriver Error!", 0)
            sys.exit() # close program if there is a chromedriver error
        time.sleep(0.5) # add a wait to allow driver to fully initialize
        driver.set_window_size(desktop['width'], desktop["height"])
        time.sleep(0.5) # add a wait to allow window to fully re-size
    if device is "M":
        mobile = {"width": 375, "height": 812} #iPhone X dimensions; can be changed to meet your device configurations
        try:
            driver = webdriver.Chrome(executable_path="Drivers\\Chromedriver\\chromedriver.exe", options=chrome_options)
        except:
            ctypes.windll.user32.MessageBoxW(0, "Program could not execute! Possible errors:\n\n1. Google Chrome v74 is not installed on your device\n2. Missing Chromedriver. Could not find \"Drivers/Chromedriver/Chromedriver.exe\" which is often the result of moving the application from the source location. To use outside its source location, \"copy\" or \"create a shortcut\" but do not move the original program from its source location unless all dependencies are moved along with it.", "Chromedriver Error!", 0)
            sys.exit() # close program if there is a chromedriver error
        time.sleep(0.5) # add a wait to allow driver to fully initialize
        driver.set_window_size(mobile['width'], mobile["height"])
        time.sleep(0.5) # add a wait to allow window to fully re-size
    if device is "T":
        tablet = {"width": 768, "height": 1024} #iPad / iPad2 / iPad Mini dimensions; can be changed to meet your device configurations
        try:
            driver = webdriver.Chrome(executable_path="Drivers\\Chromedriver\\chromedriver.exe", options=chrome_options)
        except:
            ctypes.windll.user32.MessageBoxW(0, "Program could not execute! Possible errors:\n\n1. Google Chrome v74 is not installed on your device\n2. Missing Chromedriver. Could not find \"Drivers/Chromedriver/Chromedriver.exe\" which is often the result of moving the application from the source location. To use outside its source location, \"copy\" or \"create a shortcut\" but do not move the original program from its source location unless all dependencies are moved along with it.", "Chromedriver Error!", 0)
            sys.exit() # close program if there is a chromedriver error
        time.sleep(0.5) # add a wait to allow driver to fully initialize
        driver.set_window_size(tablet['width'], tablet["height"])
        time.sleep(0.5) # add a wait to allow window to fully re-size

    return driver

def fullpage_screenshot(driver, URL, device, folder, filetype):
    print(f"Taking screenshot of {URL}")
    
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
    # saving file as name of URL (the below list covers filename forbidden characters)
    # not all below are valid URL characters but if ever functionality changed from URL to something else as the fileName, the below will cover all restrictions
    # file name can be changed below or additional restrictions handled
    fileName = URL.replace("://", "_")
    fileName = fileName.replace("\\", "_")
    fileName = fileName.replace("/", "_")
    fileName = fileName.replace(":", "_")
    fileName = fileName.replace("*", "_")
    fileName = fileName.replace("?", "_")
    fileName = fileName.replace("\"", "_")
    fileName = fileName.replace("<", "_")
    fileName = fileName.replace(">", "_")
    fileName = fileName.replace("|", "_")
    
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("  %Y-%m-%d %H_%M_%S")
    
    try:
        stitched_image.save(folder+fileName+filetype)
    except:
        fileNameExcessiveLength = True
        while fileNameExcessiveLength:
            fileName = fileName[:-1] # keep removing last character from fileName until length is short enough to be saved
            if os.path.exists(folder+fileName+filetype):
                fileName = fileName[:-21] + timestamp # if by shortening fileName the name already exists in the directory, add a timestamp to diferentiate (remove same number of characters as the timestamp from fileName)
            try:
                stitched_image.save(folder+fileName+filetype)
                fileNameExcessiveLength = False # end loop if file is saved
            except:
                fileName = fileName[:-1] # not needed again since already at top but it will speed up the process a bit
    
    del stitched_image

def btn_clicks(driver):
    # parts of the page may need to be clicked based on your screenshot needs
    # add as many try/except clauses as you need to fit all your page needs
    # examples included below - since it's a try/catch, even if elements are not on the page, the program will not crash
    try:
        BoxExpand = (driver.find_element_by_xpath("//*[contains(text(),'Expand')]")).click() # for example if a T&C box needed to be expanded to capture full text in screenshot
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
        time.sleep(0.1)                                         # header-wrapper is common bootstrap nav bar class name
    except:
        time.sleep(0.1)

def single_url(device, folder, filetype):
    URL = input("\nEnter the URL: ")

    while not URL.startswith("https://"):
        URL = input("\nInvalid URL! Please enter a URL that starts with \"https://\": ")
    
    driver = build_driver(device)
    driver.get(URL)

    btn_clicks(driver)
    fullpage_screenshot(driver, URL, device, folder, filetype)
    print("Done!")
    driver.quit()

def multiple_urls(device, folder, filetype):
    URLFile = input("\nPlease drag a \".txt\" file here containing all the URLs on a new line: ")
    
    while not URLFile.endswith(".txt"): # Can be adjusted based on your requirements. Feeding in a CSV for very large lists is recommended
        URLFile = input("\nThat is not a valid file. Please drag a \".txt\" file here: ")
    
    urlList = loadtxt(URLFile, dtype=str, comments="#", delimiter="\n", unpack=False)

    wrongURLs = ""

    for URL in urlList:
        if not URL.startswith("https://"):
            wrongURLs += URL + "\n"
    
    if wrongURLs:
        ctypes.windll.user32.MessageBoxW(0, "The following do not start with \"https://\" and must be fixed:\n\n" + wrongURLs, "Invalid URL Error!", 0)
        sys.exit()
    
    driver = build_driver(device)
    for URL in urlList:
        driver.get(URL)
        btn_clicks(driver)
        fullpage_screenshot(driver, URL, device, folder, filetype)
    
    print("Done!")
    driver.quit()

### SCREENSHOT CAPTURE ENDS HERE ###

### APPLICATION EXECUTION BEGINS HERE ###
if __name__ == '__main__':
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
    option = input("\n[1] Single URL \n[2] Multiple URLs \n[3] Close Program \n\nPlease select an option ([1]/[2]/[3]): ")

    while option not in ("1","2","3"):
        print("\nNot a valid option")
        option = input("\nPlease select an option ([1]/[2]/[3]): ")
    if option is "1":
        single_url(device, folder, filetype)
    elif option is "2":
        multiple_urls(device, folder, filetype)
    elif option is "3":
        sys.exit()

    # after all screenshots taken, open the folder containing the screenshots
    os.startfile(folder)

### APPLICATION EXECUTION ENDS HERE ###