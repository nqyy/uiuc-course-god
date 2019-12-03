UIUC course auto-register
=========================

Introduction
------------
Automatically check and register courses for students of UIUC. This software is able to bypass
the detection system of the school in a way of refreshing and updating remaining seats rather than attempting to register courses.

Warning
-------
This is a rule-breaking software, so please beware the risks.

Requirements
------------
Packages installation guide: ``pip install -r requirement.txt``

Compatible with Python2 and Python3

Requirements: bs4, selenium, chromedriver (using brew cask)

Usage and features
------------------
``python run.py netid password CRN1 CRN2 ...``

Multiple courses can be put in at the same time.

Crosslist courses are supported.

Courses with lab/discussion section are not supported.

Contributing
------------
Need to be updated for each semester. 
If there is any outdated part, please make a pull request or contact the author.
Contact me if you want to maintain this repo.

email: chitianhaoxp@gmail.com

wechat: chitianhao

Future features
---------------
1. Twilio can be added to send message for remaining seats finding and successful registration.
2. ``argparse`` or configuration file can be added. (currently the logic is straightforward so they are not involved)
3. Support of courses with lab/discussion section.

Notice
------
Created by Tianhao Chi. All rights reserved.
