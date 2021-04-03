# UIUC COURSE GOD
# course registration cheat for UIUC
# support multiple crn for different courses
# author: Tianhao Chi
# usage: python go.py semester netid password crn1 crn2 ...
# use semester in this format: YYYY-spring, YYYY-summer, YYYY-fall. Example: 2021-spring
# note: do not log in into the system by yourself while using this program

# required package: bs4, selenium, chromedriver

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import sys

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


def construct_term_in(semester):
    # This is dark magic and you will never know
    year = semester[:semester.find('-')]
    season = semester[semester.find('-')+1:]
    if season == 'spring':
        season_num = 1
    if season == 'summer':
        season_num = 2
    if season == 'fall':
        season_num = 3
    return 3 * int(year) + 114150 + season_num


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


def refresh_course_website(driver, crn_arr, cross_list, term_in):
    remaining_seat = 0
    print("start refreshing ...")
    # keep refreshing until find empty space
    while True:
        for crn in crn_arr:
            # this link needs to be updated each semester!
            url = 'https://ui2web1.apps.uillinois.edu/BANPROD1/bwckschd.p_disp_detail_sched?term_in=%d&crn_in=%s' % (
                term_in, crn)
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
    user_field = driver.find_element_by_name("USER")
    password_field = driver.find_element_by_name("PASSWORD")
    user_field.send_keys(username)
    password_field.send_keys(password)
    driver.find_element_by_name("BTN_LOGIN").click()
    return driver


# Semester needs to be updated each semester!
def navigate(driver, username, password, crn):
    year = semester[:semester.find('-')]
    season = semester[semester.find('-')+1:]
    season = season[0].capitalize() + season[1:]
    semester_str = season + ' ' + year + ' - Urbana-Champaign'

    # this url might need update
    url = "https://ui2web1.apps.uillinois.edu/BANPROD1/twbkwbis.P_GenMenu?name=bmenu.P_StuMainMnu"
    driver.get(url)
    driver.find_element_by_link_text('Classic Registration').click()
    driver.find_element_by_link_text('Add/Drop Classes').click()
    driver.find_element_by_link_text('I Agree to the Above Statement').click()

    # go to register page
    options = Select(driver.find_element_by_id('term_id'))
    options.select_by_visible_text(semester_str)
    path = '//input[@type="submit" and @value="Submit"]'
    driver.find_element_by_xpath(path).click()

# ============================================ main ===================================


# put the crn numbers into the array
crn_arr = []
for i in range(4, len(sys.argv)):
    crn_arr.append(sys.argv[i])
if(len(crn_arr) < 1):
    print("crn index error")

# login url may change and might need update in the future
login_url = 'https://login.uillinois.edu/auth/SystemLogin/sm_login.fcc?TYPE=33554433&REALMOID=06-a655cb7c-58d0-4028-b49f-79a4f5c6dd58&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=-SM-dr9Cn7JnD4pZ%2fX9Y7a9FAQedR3gjL8aBVPXnJiLeXLOpk38WGJuo%2fOQRlFkbatU7C%2b9kHQgeqhK7gmsMW81KnMmzfZ3v0paM&TARGET=-SM-HTTPS%3a%2f%2fwebprod%2eadmin%2euillinois%2eedu%2fssa%2fservlet%2fSelfServiceLogin%3fappName%3dedu%2euillinois%2eaits%2eSelfServiceLogin%26dad%3dBANPROD1'

# semester in this format: YYYY-spring/YYYY-summer/YYYY-fall
semester = sys.argv[1]
username = sys.argv[2]  # netid
password = sys.argv[3]  # password

# please change to true if the course is crosslisted
cross_list = True

start = time.time()

term_in = construct_term_in(semester)

while len(crn_arr) != 0:
    # the driver for refresh
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = log_in(username, password, driver)
    crn_success = ""
    crn_success = refresh_course_website(driver, crn_arr, cross_list, term_in)

    # if empty seat found. the driver for register
    navigate(driver, username, password, crn_success)
    register(driver, crn_success)

    msg = "time spent: %s" % (time.time() - start)
    print(msg)
    print("crn: " + crn_success + " is done!!!!!!!!!!!!!!!!!")
    crn_arr.remove(crn_success)
    driver.quit()
