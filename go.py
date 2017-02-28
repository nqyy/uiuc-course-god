from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import re
import re
import mechanize as me
import time
import sys
import urllib2
import thread
from multiprocessing.pool import ThreadPool

def check_timeout(driver, last_check_time):
    if time.time() - last_check_time <= 1800:
        return False, last_check_time
    try:
        driver.find_element_by_xpath('//input[@value="Submit Changes"]').click()
        driver.save_screenshot('after_exceed_timeout_submit.png')
        driver.find_element_by_xpath('//input[@value="Submit Changes"]')
        last_check_time = time.time()
        return False, last_check_time
    except NoSuchElementException:
        return True, last_check_time

def get_remaining_seat(soup):
    try:
        remaining_seat = soup('th', attrs={'scope':'row'})[3].find_next_siblings('td')[2].string
    except IndexError:
        remaining_seat = soup('th', attrs={'scope':'row'})[3].find_next_siblings('td')[2].string
    return int(remaining_seat)

def refresh_course_website(driver, crn):
    last_check_time = time.time()
    last_log_in_time = time.time()
    last_update_time = time.time()
    br = me.Browser()
    br.set_handle_robots(False)
    url = 'https://ui2web1.apps.uillinois.edu/BANPROD1/bwckschd.p_disp_detail_sched?term_in=120171&crn_in=%s' %crn
    response = br.open(url)
    soup = bs(response.read(), 'html.parser')
    remaining_seat = get_remaining_seat(soup)
    while remaining_seat <= 0:
        print 'course %s remaining seat: %d' %(crn, remaining_seat)
        #start = time.time()
        isTimeout, last_check_time = check_timeout(driver, last_check_time)
        if isTimeout:
            pool = ThreadPool(processes=1)
            relogin_result = pool.apply_async(go_to_add_course_page, ()) #another thread relogging
            response = br.reload()
            soup = bs(response.read(), 'html.parser')
            remaining_seat = get_remaining_seat(soup)
            msg = 'browser automatically logged out after %d seconds since last time log in' %(time.time() - last_log_in_time)
            print msg
            last_log_in_time = time.time()
            last_check_time = time.time()
            pool.close()
            pool.join()
            driver = relogin_result.get()
        else:
            if time.time() - last_update_time > 3600:
                last_update_time = time.time()
                msg = 'course %s is still alive' %crn
                print msg
                driver.save_screenshot('update.png')
            time.sleep(0.1)
            response = br.reload()
            soup = bs(response.read(), 'html.parser')
            remaining_seat = get_remaining_seat(soup)

def register(driver, crn, crn2):
    try:
        crn_blank1 = driver.find_element_by_xpath('//input[@id="crn_id1"]')
        crn_blank1.send_keys(crn)
        crn_blank2 = driver.find_element_by_xpath('//input[@id="crn_id2"]')
        crn_blank2.send_keys(crn2)
        driver.find_element_by_xpath('//input[@value="Submit Changes"]').click()
    except NoSuchElementException:
        driver = go_to_add_course_page()
        crn_blank1 = driver.find_element_by_xpath('//input[@id="crn_id1"]')
        crn_blank1.send_keys(crn)
        driver.find_element_by_xpath('//input[@value="Submit Changes"]').click()
    driver.save_screenshot('screen.png')

def log_in(username, password, driver):
    driver.get(login_url)
    user_field = driver.find_element_by_name("inputEnterpriseId")
    password_field = driver.find_element_by_name("password")
    user_field.send_keys(username)
    password_field.send_keys(password)
    driver.find_element_by_name("BTN_LOGIN").click()
    return driver

def navigate(driver, username, password, crn, major='Computer Engineering', semester='Spring 2017 - Urbana-Champaign'):
    driver.find_element_by_link_text('Registration & Records').click()
    driver.find_element_by_link_text('Classic Registration').click()
    driver.find_element_by_link_text('Add/Drop Classes').click()
    driver.find_element_by_link_text('I Agree to the Above Statement').click()

    #go to register page
    options = Select(driver.find_element_by_id('term_id'))
    options.select_by_visible_text(semester)
    path = '//input[@type="submit" and @value="Submit"]'
    driver.find_element_by_xpath(path).click()

#============================================ main ==============================================
try:
    crn2 = ""
    crn = sys.argv[1]
    crn2 = sys.argv[2]
except IndexError:
    print 'need course crn number'

login_url = 'https://eas.admin.uillinois.edu/eas/servlet/EasLogin?redirect=https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1'
username = '' #netid
password = '' #password

start = time.time()
driver = webdriver.Firefox()
def go_to_add_course_page(driver=driver, login_url=login_url, username=username, password=password, crn=crn):
    driver = log_in(username, password, driver)
    navigate(driver, username, password, crn, driver)
    return driver

i = 0
while i == 0:
    driver = go_to_add_course_page()
    msg = "restart the program over head === %s seconds ===" % (time.time() - start)
    print msg
    refresh_course_website(driver, crn)
    register(driver, crn, crn2)
    i = 1
print "done shit!!!!!!!!!!!!!!!!!"

