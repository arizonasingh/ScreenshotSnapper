"""
Author: Anmol Singh
GitHub: https://github.com/arizonasingh/ScreenshotSnapper
Purpose: To automate the process of capturing full web page screenshots in multiple viewports (desktop, mobile, tablet)
Date Created: 12 Apr 2019
"""

import os
import sys

from PyQt5 import QtCore, QtWidgets, QtGui

from screenshot_utils import capture_fullpage_screenshot
from utils import create_webdriver, get_folder, open_screenshots

DEVICE_OPTIONS = {"1": "desktop", "2": "mobile", "3": "tablet"}
FILE_TYPE_OPTIONS = {"1": ".pdf", "2": ".png"}

device = "1"  # default set to Desktop
file_extension = "2"  # default set to PNG file type
url = ""
url_file = ""
app_submit = False
screenshot = False

def set_desktop():
    global device
    device = "1"

def set_mobile():
    global device
    device = "2"

def set_tablet():
    global device
    device = "3"

def set_pdf():
    global file_extension
    file_extension = "1"

def set_png():
    global file_extension
    file_extension = "2"

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


class ScreenshotCaptureGUI(object):
    def __init__(self, device_type):
        self.driver = create_webdriver(device_type)

    def single_url(self, folder, filetype):
        global url
        global screenshot

        self.driver.get(url)

        capture_fullpage_screenshot(self.driver, url, folder, filetype)
        print("Done!")
        screenshot = True
        self.driver.quit()

    def multiple_urls(self, folder, filetype):
        global url_file
        global screenshot

        with open(url_file) as file:
            url_list = file.read().splitlines()

        wrong_urls = [url for url in url_list if not url.startswith("https://")]

        if wrong_urls:
            print("The following do not start with \"https://\" and must be fixed:\n")
            print("\n".join(wrong_urls))
            sys.exit()

        for url in url_list:
            self.driver.get(url)
            capture_fullpage_screenshot(self.driver, url, folder, filetype)

        print("Done!")
        screenshot = True
        self.driver.quit()

if __name__ == '__main__':
    ui = UiDialog()

    # executing GUI
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui.setup_ui(Dialog)
    Dialog.show()
    app.exec_()

    # after GUI closes
    if app_submit:
        device = DEVICE_OPTIONS[device]
        file_extension = FILE_TYPE_OPTIONS[file_extension]

        screenshotCapture = ScreenshotCaptureGUI(device)
        screenshot_dir = get_folder(device)

        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        if url:  # if single URL option selected from GUI
            screenshotCapture.single_url(screenshot_dir, file_extension)
        elif url_file:  # if multiple URLs option selected from GUI
            screenshotCapture.multiple_urls(screenshot_dir, file_extension)

        # after all screenshots taken, open the folder containing the screenshots
        if screenshot:
            open_screenshots(screenshot_dir)
