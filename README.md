UIUC Course God
=========================

Introduction
------------
Automatically check and register courses for UIUC students. This software is able to bypass
school's auto-detection system.

Warning
-------
This is a rule-breaking software, so please beware the risks.

Requirements
------------
Packages installation guide: ``pip3 install -r requirement.txt``

Compatible with Python2 and Python3

Requirements: bs4, selenium, chromedriver (using brew cask), webdriver-manager

Usage and features
------------------
``python3 run.py semester netid password CRN1 CRN2 ...``

Use semester in this format: YYYY-season.

Example usage: ``python3 run.py 2021-fall abc123 abcdefg12345 11111 22222``

Multiple courses can be put in at the same time.

Crosslist courses are supported. However, you'll need to edit the code to do this.

Courses with lab/discussion section are not supported.

Contributing
------------
If there is any outdated component, please make a pull request or contact the author.
Contact me if you want to maintain this repo.

Email: chitianhaoxp@gmail.com

Wechat: chitianhao

Future features
---------------
1. Twilio can be added to send message for remaining seats finding and successful registration.
2. ``argparse`` or configuration file can be added. (currently the logic is straightforward so they are not involved)
3. Support of courses with lab/discussion section.

Notice
------
Created by Tianhao Chi. All rights reserved.
