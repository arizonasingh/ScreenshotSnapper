__version__ = "1.4.2"
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
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
from numpy import loadtxt
import os, sys, time, datetime, ctypes, math
### IMPORTS END HERE ###

### GLOBAL VARIABLES BEGIN HERE ###
device = "D" # default set to Desktop
filetype = ".pdf" # default set to PDF file type
URL = ""
URLFile = ""
appSubmit = False
### GLOBAL VARIABLES END HERE ###

### GUI BEGINS HERE ###
class Ui_Dialog(object):
        def setupUi(self, Dialog):
                Dialog.setObjectName("Dialog")
                Dialog.resize(530, 409)
                self.SubmitBtn = QtWidgets.QPushButton(Dialog)
                self.SubmitBtn.setGeometry(QtCore.QRect(40, 260, 451, 61))
                self.SubmitBtn.setStyleSheet("background-color: rgb(0, 214, 0);\n"
        "color: rgb(255, 255, 255);\n"
        "font: 75 20pt \"MS Shell Dlg 2\";")
                self.SubmitBtn.setObjectName("SubmitBtn")
                self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
                self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 40, 131, 91))
                self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
                self.DeviceBox = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
                self.DeviceBox.setContentsMargins(0, 0, 0, 0)
                self.DeviceBox.setObjectName("DeviceBox")
                self.DesktopBtn = QtWidgets.QRadioButton(self.verticalLayoutWidget)
                self.DesktopBtn.setChecked(True)
                self.DesktopBtn.setObjectName("DesktopBtn")
                self.DeviceBox.addWidget(self.DesktopBtn)
                self.MobileBtn = QtWidgets.QRadioButton(self.verticalLayoutWidget)
                self.MobileBtn.setObjectName("MobileBtn")
                self.DeviceBox.addWidget(self.MobileBtn)
                self.TabletBtn = QtWidgets.QRadioButton(self.verticalLayoutWidget)
                self.TabletBtn.setObjectName("TabletBtn")
                self.DeviceBox.addWidget(self.TabletBtn)
                self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
                self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(40, 170, 131, 71))
                self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
                self.ImageFileTypeBox = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
                self.ImageFileTypeBox.setContentsMargins(0, 0, 0, 0)
                self.ImageFileTypeBox.setObjectName("ImageFileTypeBox")
                self.PDFBtn = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
                self.PDFBtn.setChecked(True)
                self.PDFBtn.setObjectName("PDFBtn")
                self.ImageFileTypeBox.addWidget(self.PDFBtn)
                self.PNGBtn = QtWidgets.QRadioButton(self.verticalLayoutWidget_2)
                self.PNGBtn.setObjectName("PNGBtn")
                self.ImageFileTypeBox.addWidget(self.PNGBtn)
                self.verticalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
                self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(230, 40, 261, 161))
                self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
                self.URLBox = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
                self.URLBox.setContentsMargins(0, 0, 0, 0)
                self.URLBox.setObjectName("URLBox")
                self.SingleURLBtn = QtWidgets.QRadioButton(self.verticalLayoutWidget_3)
                self.SingleURLBtn.setCheckable(True)
                self.SingleURLBtn.setChecked(True)
                self.SingleURLBtn.setObjectName("SingleURLBtn")
                self.URLBox.addWidget(self.SingleURLBtn)
                self.URL = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
                self.URL.setAutoFillBackground(False)
                self.URL.setText("")
                self.URL.setReadOnly(False)
                self.URL.setClearButtonEnabled(True)
                self.URL.setObjectName("URL")
                self.URLBox.addWidget(self.URL)
                self.MultipleURLsBtn = QtWidgets.QRadioButton(self.verticalLayoutWidget_3)
                self.MultipleURLsBtn.setChecked(False)
                self.MultipleURLsBtn.setObjectName("MultipleURLsBtn")
                self.URLBox.addWidget(self.MultipleURLsBtn)
                self.URLFile = QtWidgets.QLineEdit(self.verticalLayoutWidget_3)
                self.URLFile.setEnabled(False)
                self.URLFile.setAutoFillBackground(False)
                self.URLFile.setStyleSheet("")
                self.URLFile.setText("")
                self.URLFile.setReadOnly(False)
                self.URLFile.setPlaceholderText("")
                self.URLFile.setClearButtonEnabled(True)
                self.URLFile.setObjectName("URLFile")
                self.URLBox.addWidget(self.URLFile)
                self.CancelBtn = QtWidgets.QPushButton(Dialog)
                self.CancelBtn.setGeometry(QtCore.QRect(40, 340, 451, 41))
                self.CancelBtn.setStyleSheet("background-color: rgb(208, 0, 0);\n"
        "color: rgb(255, 255, 255);\n"
        "font: 75 10pt \"MS Shell Dlg 2\";")
                self.CancelBtn.setObjectName("CancelBtn")
                self.label = QtWidgets.QLabel(Dialog)
                self.label.setGeometry(QtCore.QRect(40, 10, 169, 21))
                self.label.setStyleSheet("")
                self.label.setObjectName("label")
                self.label_2 = QtWidgets.QLabel(Dialog)
                self.label_2.setGeometry(QtCore.QRect(40, 140, 129, 20))
                self.label_2.setObjectName("label_2")
                self.HelpBtn = QtWidgets.QPushButton(Dialog)
                self.HelpBtn.setGeometry(QtCore.QRect(330, 210, 161, 31))
                self.HelpBtn.setStyleSheet("background-color: rgb(245, 206, 10);\n"
        "font: 75 10pt \"MS Shell Dlg 2\";\n"
        "color: rgb(255, 255, 255);")
                self.HelpBtn.setObjectName("HelpBtn")

                self.retranslateUi(Dialog)
                QtCore.QMetaObject.connectSlotsByName(Dialog)

                ### Actionable Steps below ###
                # Set Device
                self.DesktopBtn.clicked.connect(self.setDesktop)
                self.MobileBtn.clicked.connect(self.setMobile)
                self.TabletBtn.clicked.connect(self.setTablet)

                # Set Image File Type
                self.PDFBtn.clicked.connect(self.setPDF)
                self.PNGBtn.clicked.connect(self.setPNG)

                # Handle single/multiple URL on/off
                self.SingleURLBtn.clicked.connect(self.setSingleURLBtn)
                self.MultipleURLsBtn.clicked.connect(self.setMultipleUrlsBtn)

                # Set submit and cancel
                self.SubmitBtn.clicked.connect(self.setSubmitBtn)
                self.CancelBtn.clicked.connect(self.setCancelBtn)
                self.HelpBtn.clicked.connect(self.setHelpBtn)

        def retranslateUi(self, Dialog):
                _translate = QtCore.QCoreApplication.translate
                Dialog.setWindowTitle(_translate("Dialog", "Screenshot Snapper"))
                self.SubmitBtn.setText(_translate("Dialog", "Take Screenshot"))
                self.DesktopBtn.setText(_translate("Dialog", "Desktop"))
                self.MobileBtn.setText(_translate("Dialog", "Mobile"))
                self.TabletBtn.setText(_translate("Dialog", "Tablet"))
                self.PDFBtn.setText(_translate("Dialog", "PDF"))
                self.PNGBtn.setText(_translate("Dialog", "PNG"))
                self.SingleURLBtn.setText(_translate("Dialog", "Single URL"))
                self.URL.setPlaceholderText(_translate("Dialog", "URL must start with https://"))
                self.URLFile.setPlaceholderText(_translate("Dialog", "Enter text file containing URLs"))
                self.MultipleURLsBtn.setText(_translate("Dialog", "Multiple URLs"))
                self.CancelBtn.setText(_translate("Dialog", "Close Program"))
                self.label.setText(_translate("Dialog", "SELECT A DEVICE"))
                self.label_2.setText(_translate("Dialog", "SAVE IMAGE AS"))
                self.HelpBtn.setText(_translate("Dialog", "HELP"))
        
        ### Actionable Steps below ###
        def setDesktop(self):
                global device
                device = "D"

        def setMobile(self):
                global device
                device = "M"

        def setTablet(self):
                global device
                device = "T"

        def setPDF(self):
                global filetype
                filetype = ".pdf"

        def setPNG(self):
                global filetype
                filetype = ".png"

        def setSingleURLBtn(self):
                self.URLFile.setText("") # clear out any text if any in opposite field
                self.URLFile.setEnabled(False) # then disable option for multiple urls button entry
                self.URL.setEnabled(True) # enable option for single url button entry
                
        def setMultipleUrlsBtn(self):
                self.URL.setText("") # clear out any text if any in opposite field
                self.URL.setEnabled(False) # then disable option for single url button entry
                self.URLFile.setEnabled(True) # enable option for mutiple urls button entry
                fileOptions = QtWidgets.QFileDialog.Options()
                fileOptions |= QtWidgets.QFileDialog.DontUseNativeDialog
                fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select a Text File", "", "Text Documents (*.txt)", options=fileOptions) 
                self.URLFile.setText(fileName)

        def setSubmitBtn(self):
                global URL
                URL = self.URL.text()
                global URLFile
                URLFile = self.URLFile.text()
                global appSubmit
                appSubmit = True
                Dialog.close() # close GUI if user hits submit button
        
        def setCancelBtn(self):
                sys.exit() # close program if user hits close button

        def setHelpBtn(self):
                ctypes.windll.user32.MessageBoxW(0, "Please visit https://github.com/arizonasingh/ for more documentation on how this program functions.", "HELP", 0)

### GUI ENDS HERE ###

### SCREENSHOT CAPTURE BEGINS HERE ###
class ScreenshotCapture(object):
    def build_driver(self, device):
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
                ctypes.windll.user32.MessageBoxW(0, "Program could not execute! Possible errors:\n\n1. Google Chrome v77 is not installed on your device\n2. Missing Chromedriver. Could not find \"Drivers/Chromedriver/Chromedriver.exe\" which is often the result of moving the application from the source location. To use outside its source location, \"copy\" or \"create a shortcut\" but do not move the original program from its source location unless all dependencies are moved along with it.", "Chromedriver Error!", 0)
                sys.exit() # close program if there is a chromedriver error
            time.sleep(0.5) # add a wait to allow driver to fully initialize
            driver.set_window_size(desktop['width'], desktop["height"])
            time.sleep(0.5) # add a wait to allow window to fully re-size
        if device is "M":
            mobile = {"width": 375, "height": 812} #iPhone X dimensions; can be changed to meet your device configurations
            try:
                driver = webdriver.Chrome(executable_path="Drivers\\Chromedriver\\chromedriver.exe", options=chrome_options)
            except:
                ctypes.windll.user32.MessageBoxW(0, "Program could not execute! Possible errors:\n\n1. Google Chrome v77 is not installed on your device\n2. Missing Chromedriver. Could not find \"Drivers/Chromedriver/Chromedriver.exe\" which is often the result of moving the application from the source location. To use outside its source location, \"copy\" or \"create a shortcut\" but do not move the original program from its source location unless all dependencies are moved along with it.", "Chromedriver Error!", 0)
                sys.exit() # close program if there is a chromedriver error
            time.sleep(0.5) # add a wait to allow driver to fully initialize
            driver.set_window_size(mobile['width'], mobile["height"])
            time.sleep(0.5) # add a wait to allow window to fully re-size
        if device is "T":
            tablet = {"width": 768, "height": 1024} #iPad / iPad2 / iPad Mini dimensions; can be changed to meet your device configurations
            try:
                driver = webdriver.Chrome(executable_path="Drivers\\Chromedriver\\chromedriver.exe", options=chrome_options)
            except:
                ctypes.windll.user32.MessageBoxW(0, "Program could not execute! Possible errors:\n\n1. Google Chrome v77 is not installed on your device\n2. Missing Chromedriver. Could not find \"Drivers/Chromedriver/Chromedriver.exe\" which is often the result of moving the application from the source location. To use outside its source location, \"copy\" or \"create a shortcut\" but do not move the original program from its source location unless all dependencies are moved along with it.", "Chromedriver Error!", 0)
                sys.exit() # close program if there is a chromedriver error
            time.sleep(0.5) # add a wait to allow driver to fully initialize
            driver.set_window_size(tablet['width'], tablet["height"])
            time.sleep(0.5) # add a wait to allow window to fully re-size

        return driver

    def fullpage_screenshot(self, driver, url, device, folder, filetype):
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

        stitched_image = Image.new('RGB',(int(viewport_width * scale), int(total_height * scale)))
        
        for j, rectangle in enumerate(rectangles):
            driver.execute_script(f"window.scrollTo({0}, {rectangle[1]})")
            time.sleep(0.2)

            tmpImgName = f"section_{j}.png"
            driver.get_screenshot_as_file(tmpImgName)
            screenshot = Image.open(tmpImgName)

            self.remove_sticky_navs(driver)

            if (j + 1) * viewport_height > total_height:
                offset = (0, int((total_height - viewport_height) * scale))
            else:
                offset = (0, int(j * viewport_height * scale - math.floor(j / 2.0)))

            stitched_image.paste(screenshot, offset)

            del screenshot
            os.remove(tmpImgName)

        # files have naming restrictions
        # saving file as name of url (the below list covers filename forbidden characters)
        # not all below are valid URL characters but if ever functionality changed from URL to something else as the fileName, the below will cover all restrictions
        # file name can be changed below or additional restrictions handled
        fileName = url.replace("://", "_")
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

    def btn_clicks(self, driver):
        # parts of the page may need to be clicked based on your screenshot needs
        # add as many try/except clauses as you need to fit all your page needs
        # examples included below - since it's a try/catch, even if elements are not on the page, the program will not crash
        try:
            BoxExpand = (driver.find_element_by_xpath("//*[contains(text(),'Expand')]")).click() # for example if a T&C box needed to be expanded to capture full text in screenshot
        except:
            time.sleep(0.1)
        
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME) # returning to top of page after clicking buttons

    def remove_sticky_navs(self, driver):
        # many pages will have at least one sticky nav bar
        # unless they are removed or their position is set, the nav bar will appear multiple times in the screenshot
        # add as many try/except clauses as you need to fit all your page needs
        # examples included below - since it's a try/catch, even if elements are not on the page, the program will not crash
        try:
            driver.execute_script("$('.header-wrapper').remove();") # nav bar can be removed or fixed into place (static or absolute work in most cases for position property - try .attr('style','position: static !important'); instead of .remove();)
            time.sleep(0.1)                                         # header-wrapper is common bootstrap nav bar class name
        except:
            time.sleep(0.1)

    def single_url(self, device, folder, filetype):
        global URL

        while not URL.startswith("https://"):
            ctypes.windll.user32.MessageBoxW(0, "The URL entered does not start with \"https://\" and must be fixed:\n\n" + URL, "Invalid URL Error!", 0)
            sys.exit()
        
        driver = self.build_driver(device)
        driver.get(URL)

        self.btn_clicks(driver)
        self.fullpage_screenshot(driver, URL, device, folder, filetype)
        print("Done!")
        driver.quit()

    def multiple_urls(self, device, folder, filetype):
        global URLFile
        
        urlList = loadtxt(URLFile, dtype=str, comments="#", delimiter="\n", unpack=False)

        wrongURLs = ""

        for url in urlList:
            if not url.startswith("https://"):
                wrongURLs += url + "\n"
        
        if wrongURLs:
            ctypes.windll.user32.MessageBoxW(0, "The following do not start with \"https://\" and must be fixed:\n\n" + wrongURLs, "Invalid URL Error!", 0)
            sys.exit()
        
        driver = self.build_driver(device)
        for url in urlList:
            driver.get(url)
            self.btn_clicks(driver)
            self.fullpage_screenshot(driver, url, device, folder, filetype)
        
        print("Done!")
        driver.quit()

### SCREENSHOT CAPTURE ENDS HERE ###

### APPLICATION EXECUTION BEGINS HERE ###
if __name__ == '__main__':
    ui = Ui_Dialog()
    ss = ScreenshotCapture()

    # executing GUI
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    app.exec_()

    # after GUI closes
    if appSubmit:
        if device is "D":
            folder = "Screenshots\\Desktop\\"
        if device is "M":
            folder = "Screenshots\\Mobile\\"
        if device is "T":
            folder = "Screenshots\\Tablet\\"

        if not os.path.exists(folder):
            os.makedirs(folder)

        if URL: # if single URL option selected from GUI
            ss.single_url(device, folder, filetype)
        elif URLFile: # if multiple URLs option selected from GUI
            ss.multiple_urls(device, folder, filetype)

        # after all screenshots taken, open the folder containing the screenshots
        os.startfile(folder)

### APPLICATION EXECUTION ENDS HERE ###