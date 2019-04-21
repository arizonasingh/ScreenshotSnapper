# ScreenshotSnapper
Allows for webpage screenshot automation for desktop, mobile, and tablet viewports

Example screenshots included!

## Prerequisites:
1. Should only be run on Windows machine
2. Screen resolution of 1920x1080 should look good (text and apps are not blurry) on your machine (can be changed within the script)

NOTE: Chromedriver73 is included in this repo. It's included in the repo so executable works out the box. When making changes specific to your program needs, the program can be freezed with the path of the chromedriver so the program works for anyone who receives the full repo distribution. If using only for yourself, it's better to add chromedriver to your PATH.

## Additional Details:
If you encounter sticky nav bars on the webpage, you must enter javascript code into the webpage to handle those. Since those are different for each webpage, I have included a couple examples in the code to show how it should be done and where it should be done. The same goes for any page interactions needed on the page before screen capture such as clicking a button.

If you have a very large list of URLs to feed into the script, I recommend using CSV instead of Text file. Small configuration will need to be made for that.

Mobile Emulation instead of browser window re-sizing is possible, however with the current implementation, it's incompatible with the screen capture feature. I have commented out where the mobile emulation should be done and how it should be done if anyone wants to tackle it. If you are able to make it work, please push a version to this repo so I may see and test.

This can be used by many professionals who have to take screenshots of webpages frequently. Often times, many non-technical people will also benefit from such a program. This program is meant to be shared with all people, especially those non-technical people who could really benefit from such a tool. If you intend to share across to those people, I recommend providing it as an executable (I recommend PyInstaller to freeze or package the code). This program can also be of great use to automation testers who have to take many screen captures (especially of different viewports) for their job duties.

Special thanks to this willjobs of https://github.com/willjobs/fullpage-screenshot
The code for screen capture and page scrolling (key feature) was adapted from that repo.

Please do not contact me to make a version for you with your exact web needs. I have tried to make it as easy as possible for customization with many comments throughout the code. I have a Full-Time job and unfortunately cannot create unique versions for everyone. However, if there are any questions or inquiries, I will try and monitor this repo in my spare time and answer to the best of my knowledge or ability.

Have fun taking screenshots!
