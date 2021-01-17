__version__ = "3.0.0"
"""
Author: Anmol Singh
GitHub: https://github.com/arizonasingh/ScreenshotSnapper
Purpose: To automate the process of capturing full web page screenshots in multiple viewports (desktop, mobile, tablet)
Date Created: 12 Apr 2019
"""

### IMPORTS BEGIN HERE ###
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from PyQt5 import QtCore, QtWidgets, QtGui
from PIL import Image
from pathlib import Path
import os
import sys
import time
import datetime
import math
### IMPORTS END HERE ###

### GLOBAL VARIABLES BEGIN HERE ###
device = "D"  # default set to Desktop
filetype = ".pdf"  # default set to PDF file type
url = ""
url_file = ""
app_submit = False
screenshot = False
### GLOBAL VARIABLES END HERE ###

### GUI BEGINS HERE ###
def set_desktop():
    global device
    device = "D"


def set_mobile():
    global device
    device = "M"


def set_tablet():
    global device
    device = "T"


def set_pdf():
    global filetype
    filetype = ".pdf"


def set_png():
    global filetype
    filetype = ".png"


### GUI BEGINS HERE ###
class UiDialog(object):
    def setup_ui(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(530, 429)
        self.SubmitBtn = QtWidgets.QPushButton(Dialog)
        self.SubmitBtn.setGeometry(QtCore.QRect(40, 260, 451, 61))
        self.SubmitBtn.setStyleSheet("background-color: rgb(92, 184, 92);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "font: 75 20pt \"Helvetica\";")
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
        self.URL.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^https://.*$"), self.URL))
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
        self.CancelBtn.setGeometry(QtCore.QRect(40, 340, 451, 61))
        self.CancelBtn.setStyleSheet("background-color: rgb(217, 83, 79);\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "font: 75 20pt \"Helvetica\";")
        self.CancelBtn.setObjectName("CancelBtn")
        self.DeviceLabel = QtWidgets.QLabel(Dialog)
        self.DeviceLabel.setGeometry(QtCore.QRect(40, 10, 169, 21))
        self.DeviceLabel.setStyleSheet("")
        self.DeviceLabel.setObjectName("label")
        self.FileTypeLabel = QtWidgets.QLabel(Dialog)
        self.FileTypeLabel.setGeometry(QtCore.QRect(40, 140, 129, 20))
        self.FileTypeLabel.setObjectName("label_2")

        self.retranslate_ui(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        ### Actionable Steps below ###
        # Set Device
        self.DesktopBtn.clicked.connect(set_desktop)
        self.MobileBtn.clicked.connect(set_mobile)
        self.TabletBtn.clicked.connect(set_tablet)

        # Set Image File Type
        self.PDFBtn.clicked.connect(set_pdf)
        self.PNGBtn.clicked.connect(set_png)

        # Handle single/multiple URL on/off
        self.SingleURLBtn.clicked.connect(self.set_single_url_btn)
        self.MultipleURLsBtn.clicked.connect(self.set_multiple_urls_btn)

        # Set submit and cancel
        self.SubmitBtn.clicked.connect(self.set_submit_btn)
        self.CancelBtn.clicked.connect(self.set_cancel_btn)

    def retranslate_ui(self, Dialog):
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
        self.DeviceLabel.setText(_translate("Dialog", "SELECT A DEVICE"))
        self.FileTypeLabel.setText(_translate("Dialog", "SAVE IMAGE AS"))

    ### Actionable Steps below ###

    def set_single_url_btn(self):
        self.URLFile.setText("")  # clear out any text if any in opposite field
        self.URLFile.setEnabled(False)  # then disable option for multiple urls button entry
        self.URL.setEnabled(True)  # enable option for single url button entry

    def set_multiple_urls_btn(self):
        self.URL.setText("")  # clear out any text if any in opposite field
        self.URL.setEnabled(False)  # then disable option for single url button entry
        self.URLFile.setEnabled(True)  # enable option for multiple urls button entry
        file_options = QtWidgets.QFileDialog.Options()
        file_options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select a Text File", "", "Text Documents (*.txt)",
                                                            options=file_options)
        self.URLFile.setText(filename)

    def set_submit_btn(self):
        global url
        url = self.URL.text()
        global url_file
        url_file = self.URLFile.text()
        if not (url.startswith("https://")) and not (url_file.endswith(".txt")):
            print("Only .txt files supported")
        elif not len(url_file) == 0 and not os.path.exists(url_file):
            print("That is not a valid file path to a text document")
        else:
            global app_submit
            app_submit = True
        Dialog.close()  # close GUI if user hits submit button

    def set_cancel_btn(self):
        sys.exit()  # close program if user hits close button

### GUI ENDS HERE ###

### SCREENSHOT CAPTURE BEGINS HERE ###
class ScreenshotCapture(object):
    def build_driver(self, device):
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
        chrome_options.add_argument(
            "log-level=3")  # Determines which console logs should be shown. Set to 0 for all messages, 1 for INFO
        # and above, 2 for ERROR and above, and 3 for FATAL
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.headless = True  # Set to true to run the program in the background (multi-tasking on other
        # tasks is possible). Set to false to see the program running (warning: browser will open on screen so
        # multi-tasking is not recommended as it will most likely affect the screen capture)

        # I am re-sizing the browser window to meet specific device type dimensions
        if device == "D":
            desktop = {"width": 1920,
                       "height": 1080}  # Should match the screen resolution size for a fully expanded browser
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            time.sleep(0.5)  # add a wait to allow driver to fully initialize
            driver.set_window_size(desktop['width'], desktop["height"])
            time.sleep(0.5)  # add a wait to allow window to fully re-size
        if device == "M":
            mobile = {"width": 375,
                      "height": 812}  # iPhone X dimensions; can be changed to meet your device configurations
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            time.sleep(0.5)  # add a wait to allow driver to fully initialize
            driver.set_window_size(mobile['width'], mobile["height"])
            time.sleep(0.5)  # add a wait to allow window to fully re-size
        if device == "T":
            tablet = {"width": 768,
                      "height": 1024}  # iPad / iPad2 / iPad Mini dimensions; can be changed to meet your device
            # configurations
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            time.sleep(0.5)  # add a wait to allow driver to fully initialize
            driver.set_window_size(tablet['width'], tablet["height"])
            time.sleep(0.5)  # add a wait to allow window to fully re-size

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

        stitched_image = Image.new('RGB', (int(viewport_width * scale), int(total_height * scale)))

        for j, rectangle in enumerate(rectangles):
            driver.execute_script(f"window.scrollTo({0}, {rectangle[1]})")
            time.sleep(0.2)

            tmp_img_name = f"section_{j}.png"
            driver.get_screenshot_as_file(tmp_img_name)
            screenshot = Image.open(tmp_img_name)

            self.remove_sticky_navs(driver)

            if (j + 1) * viewport_height > total_height:
                offset = (0, int((total_height - viewport_height) * scale))
            else:
                offset = (0, int(j * viewport_height * scale - math.floor(j / 2.0)))

            stitched_image.paste(screenshot, offset)

            del screenshot
            os.remove(tmp_img_name)

        # files have naming restrictions so saving file as the name of the URL (the below list covers filename
        # forbidden characters). Not all below are valid URL characters but if ever functionality changed from URL to
        # something else as the filename, the below will cover all restrictions. The file name can be changed below
        # or additional restrictions handled
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

        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("  %Y-%m-%d %H_%M_%S")

        image_path = Path.joinpath(folder, filename + filetype)
        try:
            stitched_image.save(image_path)
        except:
            filename_excessive_length = True
            while filename_excessive_length:
                filename = filename[
                           :-1]  # keep removing last character from filename until length is short enough to be saved
                if os.path.exists(image_path):
                    filename = filename[
                               :-21] + timestamp  # if by shortening filename the name already exists in the
                    # directory, add a timestamp to diferentiate (remove same number of characters as the timestamp
                    # from filename)
                try:
                    stitched_image.save(image_path)
                    filename_excessive_length = False  # end loop if file is saved
                except:
                    filename = filename[
                               :-1]  # not needed again since already at top but it will speed up the process a bit

        del stitched_image

    def btn_clicks(self, driver):
        # parts of the page may need to be clicked based on your screenshot needs add as many try/except clauses as
        # you need to fit all your page needs examples included below - since it's a try/catch, even if elements are
        # not on the page, the program will not crash
        try:
            (driver.find_element_by_xpath(
                "//*[contains(text(),'Expand')]")).click()  # for example if a T&C box needed to be expanded to
            # capture full text in screenshot
        except:
            time.sleep(0.1)

        driver.find_element_by_tag_name('body').send_keys(
            Keys.CONTROL + Keys.HOME)  # returning to top of page after clicking buttons

    def remove_sticky_navs(self, driver):
        # many pages will have at least one sticky nav bar unless they are removed or their position is set,
        # the nav bar will appear multiple times in the screenshot add as many try/except clauses as you need to fit
        # all your page needs examples included below - since it's a try/catch, even if elements are not on the page,
        # the program will not crash
        try:
            driver.execute_script(
                "$('.header-wrapper').remove();")  # nav bar can be removed or fixed into place (static or absolute
            # work in most cases for position property - try .attr('style','position: static !important'); instead of
            # .remove();)
            time.sleep(0.1)  # header-wrapper is common bootstrap nav bar class name
        except:
            time.sleep(0.1)

    def single_url(self, device, folder, filetype):
        global url
        global screenshot

        driver = self.build_driver(device)
        driver.get(url)

        self.btn_clicks(driver)
        self.fullpage_screenshot(driver, url, device, folder, filetype)
        print("Done!")
        screenshot = True
        driver.quit()

    def multiple_urls(self, device, folder, filetype):
        global url_file
        global screenshot

        url_list = open(url_file).read().splitlines()
        wrong_urls = ""

        for url in url_list:
            if not url.startswith("https://"):
                wrong_urls += url + "\n"

        if wrong_urls:
            print("The following do not start with \"https://\" and must be fixed:\n\n" + wrong_urls)
        else:
            driver = self.build_driver(device)
            for url in url_list:
                driver.get(url)
                self.btn_clicks(driver)
                self.fullpage_screenshot(driver, url, device, folder, filetype)

            print("Done!")
            screenshot = True
            driver.quit()


### SCREENSHOT CAPTURE ENDS HERE ###

def open_screenshots(folder):
    if sys.platform == "win32":
        os.startfile(folder)
    elif sys.platform == "darwin":
        os.system('open "%s"' % folder)
    elif sys.platform == "linux":
        os.system('xdg-open "%s"' % folder)

### APPLICATION EXECUTION BEGINS HERE ###
if __name__ == '__main__':
    ui = UiDialog()
    ss = ScreenshotCapture()

    # executing GUI
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui.setup_ui(Dialog)
    Dialog.show()
    app.exec_()

    # after GUI closes
    if app_submit:
        if device == "D":
            folder = Path("Screenshots/Desktop")
        if device == "M":
            folder = Path("Screenshots/Mobile")
        if device == "T":
            folder = Path("Screenshots/Tablet")

        if not os.path.exists(folder):
            os.makedirs(folder)

        if url:  # if single URL option selected from GUI
            ss.single_url(device, folder, filetype)
        elif url_file:  # if multiple URLs option selected from GUI
            ss.multiple_urls(device, folder, filetype)

        # after all screenshots taken, open the folder containing the screenshots
        if screenshot:
            open_screenshots(folder)

### APPLICATION EXECUTION ENDS HERE ###
