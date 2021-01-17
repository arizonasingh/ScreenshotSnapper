# ScreenshotSnapper
Allows for webpage screenshot automation for desktop, mobile, and tablet viewports

Example screenshots included!

## Key points to keep in mind:
1. All webpages should be responsive
2. Maximum supported image dimension is 65500 pixels

## Additional Details:
If you encounter sticky nav bars on the webpage, you must enter javascript into the webpage to handle those (this can be done via the program). Since those are different for each webpage, I have included a couple examples in the code to show how it should be done and where it should be done. The same goes for any page interactions needed on the page before screen capture such as clicking a button.

This can be used by many professionals who have to take screenshots of webpages frequently. Often times, many non-technical people will also benefit from such a program. This program is meant to be shared with all people, especially those non-technical people who could really benefit from such a tool. If you intend to share across to those people, I recommend providing it as an executable (I recommend PyInstaller to freeze or package the code). The GUI version will be especially helpful for those non-technical people. This program can also be of great use to automation testers who have to take many screen captures (especially of different viewports) for their daily job duties.

## Acknowledgements:
Special thanks to MrColes of https://mrcoles.com/full-page-screen-capture-chrome-extension/ for giving me inspiration.
I use the Google Chrome extension heavily but wanted to automate the process so I made this program.

Special thanks to this willjobs of https://github.com/willjobs/fullpage-screenshot.
The code for screen capture and page scrolling (key feature) was adapted from that repo.
