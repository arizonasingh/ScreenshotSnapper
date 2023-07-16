# ScreenshotSnapper 📷
**Enables automated webpage screenshot capture for desktop, mobile, and tablet viewports** (example screenshots included).

This program can be beneficial for professionals who frequently need to take screenshots of webpages. Additionally, many non-technical individuals can also benefit from this program. It is designed to be shared with everyone, especially those who are not technically inclined and would greatly benefit from such a tool. If you plan to share it with these individuals, I suggest providing it as an executable. The GUI version will be particularly useful for non-technical users. Automation testers who need to capture multiple screens (especially in different viewports) as part of their daily job duties will also find this program extremely valuable.

## Important Considerations for Use:
All webpages should have a responsive design

The maximum supported image dimension is 65500 pixels

If you encounter sticky nav bars on the webpage, you must insert javascript into the webpage to handle them (this can be accomplished through the program). As these type of sticky navigation bars differ for each webpage, I have included a few code examples to demonstrate how and where it should be done. The same applies to any necessary page interactions prior to screen capture, such as button clicks to expand any hidden sections. Since each user will have their own requirements based on the webpage they want to capture, I have not bundled the out-of-the-box application into an executable. Once you input your requirements, I recommend using [PyInstaller](https://pyinstaller.org/en/stable/) to freeze or package the code into an executable for your specific operating system platform.

## Acknowledgements:
Special thanks to MrColes of https://mrcoles.com/full-page-screen-capture-chrome-extension/ for giving me inspiration.
I have utilized the Google Chrome extension frequently, but I wanted to automate the process, so I created this program.

Special thanks to this willjobs of https://github.com/willjobs/fullpage-screenshot.
The code for screen capture and page scrolling (key feature) was adapted from that repo.
