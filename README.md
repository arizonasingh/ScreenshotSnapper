# ScreenshotSnapper
Allows for webpage screenshot automation for desktop, mobile, and tablet viewports

Prerequisites:
1. Should only be run on Windows machine
2. Chrome webdriver should be in your PATH (you can also have it outside your path, just enter in the directory location as a parameter in the code when initializing the webdriver)
3. Screen resolution of 1920x1080 should look good (text and apps are not blurry) on your machine (can be changed within the script)

If you encounter sticky nav bars on the webpage, you must enter javascript code into the webpage to handle those. Since those are different for each webpage, I have included a couple examples in the code to show how it should be done and where it should be done. The same goes for any page interactions needed on the page before screen capture such as clicking a button.

If you have a very large list of URLs to feed into the script, I recommend using CSV instead of Text file. Small configuration will need to be made for that.

Mobile Emulation instead of browser window re-sizing is possible, however with the current implementation, it's incompatible with the screen capture feature. I have commented out where the mobile emulation should be done and how it should be done if anyone wants to tackle it. If you are able to make it work, please push a version to this repo so I may see and test.

This can be used by many professionals who have to take screenshots of webpages frequently. Often times, many non-technical people will also benefit from such a program. This program is meant to be shared with all people, especially those non-technical people who could really benefit from such a tool. If you intend to share across to those people, I recommend providing as an executable (I prefer PyInstaller to freeze or package my code). If you convert to an executable, include chrome webdriver with the app (change the directory path in the code) and include any javascript executions (i.e. for sticky navs) that you think they may need. This program can also be of great use to automation testers who have to take many screen captures (especially of different viewports) for their job duties.

Special thanks to this Stack Overflow thread: https://stackoverflow.com/questions/41721734/take-screenshot-of-full-page-with-selenium-python-with-chromedriver
The code for scrolling on the page (key feature) was adapted from that thread. The rest of the code was developed entirely by me.

Please do not contact me to make a version for you with your exact web needs. I have tried to make it as easy as possible for customization with many comments throughout the code. I have a Full-Time job and cannot create unique versions for everyone. However, if there are any questions or inquiries, I will try and monitor this repo in my spare time and answer to the best of my knowledge or ability.

Have fun taking screenshots!
