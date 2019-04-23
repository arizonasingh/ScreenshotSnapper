# ScreenshotSnapper
Allows for webpage screenshot automation for desktop, mobile, and tablet viewports

Example screenshots included!

## Prerequisites:
1. If using Windows OS, Screen resolution of 1920x1080 should look good (text and apps are not blurry) on your machine (can be changed within the script).
2. Google Chrome v73 or higher should be installed.
3. All webpages should be responsive.

NOTE: This repo has only be tested on Windows OS, however this is nothing to suggest that this program is not platform independent. It should work for all OS. If not, slight adjustments can be made easily to adapt to OS needs. However, is using a non-Windows OS, the program will not be able to adjust the screen resolution which may or may not affect the screenshots depending on your device. Example screenshots are included - can be used for comparison if using a different OS than Windows. 

NOTE: Google Chrome version 73 or higher should be installed on your computer. Chromedriver73 is included in this repo. It's included in the repo so the executable works out the box. When making changes specific to your program needs, the program can be freezed with the local path of the chromedriver so the program works for anyone who receives the full repo distribution. If using only for yourself, it's better to add chromedriver to your PATH. It can also be freezed and packages as an executable with chromedriver within the program, but for the purposes of this repo, I did not do that as some people may not know how to do that as easily as just referencing the local path of the chromedriver.

## Additional Details:
If you encounter sticky nav bars on the webpage, you must enter javascript into the webpage to handle those (this can be done via the program). Since those are different for each webpage, I have included a couple examples in the code to show how it should be done and where it should be done. The same goes for any page interactions needed on the page before screen capture such as clicking a button.

If you have a very large list of URLs to feed into the script, I recommend using a CSV instead of a Text file. Small configurations will need to be made to handle CSV files if you choose that route.

Mobile Emulation instead of browser window re-sizing is possible, however with the current implementation, it's incompatible with the screen capture feature. I have commented out where the mobile emulation should be done and how it should be done if anyone wants to tackle it. If you are able to make it work, please push a version to this repo so I may see and test.

This can be used by many professionals who have to take screenshots of webpages frequently. Often times, many non-technical people will also benefit from such a program. This program is meant to be shared with all people, especially those non-technical people who could really benefit from such a tool. If you intend to share across to those people, I recommend providing it as an executable (I recommend PyInstaller to freeze or package the code). The GUI version will be especially helpful for those non-technical people. This program can also be of great use to automation testers who have to take many screen captures (especially of different viewports) for their daily job duties.

## Acknowledgements:
Special thanks to MrColes of https://mrcoles.com/full-page-screen-capture-chrome-extension/ for giving me inspiration.
I use the Google Chrome extension heavily but wanted to automate the process so I made this program.

Special thanks to this willjobs of https://github.com/willjobs/fullpage-screenshot.
The code for screen capture and page scrolling (key feature) was adapted from that repo.

## Final Remarks:
Please do not contact me to make a version for you with your exact web needs. I have tried to make it as easy as possible for customization with many comments throughout the code. I have a Full-Time job and unfortunately cannot create unique versions for everyone. However, if there are any questions or inquiries, I will try and monitor this repo in my spare time and answer to the best of my ability.

Have fun taking screenshots! :)
