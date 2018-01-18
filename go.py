# course registration helper for UIUC
# support multiple crn for different courses
# author: Tianhao Chi
# usage: python go.py netid password crn1 ...
# note: do not log in by yourself while using this program

# required package: bs4, selenium, chromedriver

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import sys
import urllib2

def get_remaining_seat(soup):
    try:
        # for cross list courses
        remaining_seat = soup('th', attrs={'scope':'row'})[3].find_next_siblings('td')[2].string
    except IndexError:
        # normal course registration
        remaining_seat = soup('th', attrs={'scope':'row'})[1].find_next_siblings('td')[2].string
    return int(remaining_seat)

def refresh_course_website(driver, crn):
    remaining_seat = 0
    print "start refreshing ..."
    # keep refreshing until find empty space
    while remaining_seat <= 0:
        url = 'https://ui2web1.apps.uillinois.edu/BANPROD1/bwckschd.p_disp_detail_sched?term_in=120181&crn_in=%s' %crn
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        remaining_seat = get_remaining_seat(soup)
    print "refreshing done!"

def register(driver, crn, crn_arr):
    #register the course
    for i in range(len(crn_arr)):
        xpath = "//input[@id = 'crn_id" + str(i+1) + "']"
        crn_blank = driver.find_element_by_xpath(xpath)
        crn_blank.send_keys(crn_arr[i])
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

def navigate(driver, username, password, crn, major='Computer Engineering', semester='Spring 2018 - Urbana-Champaign'):
    driver.find_element_by_link_text('Registration & Records').click()
    driver.find_element_by_link_text('Classic Registration').click()
    driver.find_element_by_link_text('Add/Drop Classes').click()
    driver.find_element_by_link_text('I Agree to the Above Statement').click()

    #go to register page
    options = Select(driver.find_element_by_id('term_id'))
    options.select_by_visible_text(semester)
    path = '//input[@type="submit" and @value="Submit"]'
    driver.find_element_by_xpath(path).click()

#============================================ main ===================================

crn_arr = []
for i in range(3, len(sys.argv)):
    crn_arr.append(sys.argv[i])
if(len(crn_arr) < 1):
    print "crn index error"
crn = sys.argv[3] #crn is the leading crn

login_url = 'https://eas.admin.uillinois.edu/eas/servlet/EasLogin?redirect=https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1'

username = sys.argv[1] #netid
password = sys.argv[2] #password

start = time.time()

# the driver for refresh
driver = webdriver.Chrome()
driver = log_in(username, password, driver)
refresh_course_website(driver, crn)

# if empty seat found. the driver for register
driver = log_in(username, password, driver)
navigate(driver, username, password, crn)
register(driver, crn, crn_arr)

msg = "time spent: %s" % (time.time() - start)
print msg
print "done!!!!!!!!!!!!!!!!!"

