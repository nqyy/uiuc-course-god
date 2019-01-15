# course registration helper for UIUC
# support multiple crn for different courses
# author: Tianhao Chi
# usage: python go.py netid password crn1 crn2 ...
# note: do not log in into the system by yourself while using this program
# Any commercial use is prohibited

# required package: bs4, selenium, chromedriver

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import sys

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


def get_remaining_seat(soup, cross_list):
    if cross_list:
        try:
            # for cross list courses
            remaining_seat = soup('th', attrs={'scope': 'row'})[
                3].find_next_siblings('td')[2].string
        except IndexError:
            remaining_seat = soup('th', attrs={'scope': 'row'})[
                1].find_next_siblings('td')[2].string
    else:
        remaining_seat = soup('th', attrs={'scope': 'row'})[
            1].find_next_siblings('td')[2].string
    return int(remaining_seat)


def refresh_course_website(driver, crn_arr, cross_list):
    remaining_seat = 0
    print("start refreshing ...")
    # keep refreshing until find empty space
    while True:
        for crn in crn_arr:
            # this link needs to be updated each semester!
            url = 'https://ui2web1.apps.uillinois.edu/BANPROD1/bwckschd.p_disp_detail_sched?term_in=120191&crn_in=%s' % crn
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            remaining_seat = get_remaining_seat(soup, cross_list)
            if remaining_seat > 0:
                print("refreshing done!")
                return crn


def register(driver, crn):
    # register single course
    xpath = "//input[@id = 'crn_id1']"
    crn_blank = driver.find_element_by_xpath(xpath)
    crn_blank.send_keys(crn)
    driver.find_element_by_xpath("//input[@value='Submit Changes']").click()
    driver.save_screenshot('screen.png')


def log_in(username, password, driver):
    driver.get(login_url)
    user_field = driver.find_element_by_name("inputEnterpriseId")
    password_field = driver.find_element_by_name("password")
    user_field.send_keys(username)
    password_field.send_keys(password)
    driver.find_element_by_name("BTN_LOGIN").click()
    return driver

# Semester needs to be updated each semester!


def navigate(driver, username, password, crn, semester='Spring 2019 - Urbana-Champaign'):
    # this url might need update
    url = "https://ui2web1.apps.uillinois.edu/BANPROD1/twbkwbis.P_GenMenu?name=bmenu.P_StuMainMnu"
    driver.get(url)
    driver.find_element_by_link_text('Classic Registration').click()
    driver.find_element_by_link_text('Add/Drop Classes').click()
    driver.find_element_by_link_text('I Agree to the Above Statement').click()

    # go to register page
    options = Select(driver.find_element_by_id('term_id'))
    options.select_by_visible_text(semester)
    path = '//input[@type="submit" and @value="Submit"]'
    driver.find_element_by_xpath(path).click()

# ============================================ main ===================================


# put the crn numbers into the array
crn_arr = []
for i in range(3, len(sys.argv)):
    crn_arr.append(sys.argv[i])
if(len(crn_arr) < 1):
    print("crn index error")

# login url may change and might need update in the future
login_url = 'https://eas.admin.uillinois.edu/eas/servlet/EasLogin?redirect=https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1'

username = sys.argv[1]  # netid
password = sys.argv[2]  # password

# please change to true if the course is crosslisted
cross_list = True

start = time.time()

while len(crn_arr) != 0:
    # the driver for refresh
    driver = webdriver.Chrome()
    driver = log_in(username, password, driver)
    crn_success = ""
    crn_success = refresh_course_website(driver, crn_arr, cross_list)

    # if empty seat found. the driver for register
    navigate(driver, username, password, crn_success)
    register(driver, crn_success)

    msg = "time spent: %s" % (time.time() - start)
    print(msg)
    print("crn: " + crn_success + " is done!!!!!!!!!!!!!!!!!")
    crn_arr.remove(crn_success)
    driver.quit()
