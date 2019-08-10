"""
Script for downloading lectures from an echo360 page
made in august 2019

Takes the URL, username (email), password as required cmd line args.
Takes optional 4th command line arg for number of initial videos to skip 
(eg if script didn't complete previously, can start again where left off).

Uses chromedriver (make sure its available in PATH and appropriate version for chrome version installed)
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import time

try:
    assert len(sys.argv>=4)
except AssertionError as e:
    print("please include at least 3 cmd line args: URL, username/email, pw")
    print(e)

#full URL of the echo360page
url = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

#set skipVideos if we've stated we want to skip some by giving a 4th cmd line arg
skipVideos = 0
if len(sys.argv)>4:
    skipVideos = int(sys.argv[4])

driver = webdriver.Chrome()
driver.get(url)

#login page
assert "Email" in driver.title
elem = driver.find_element_by_id("email")
elem.clear()
elem.send_keys("username")
elem.send_keys(Keys.RETURN)

#unimelb sso page
assert "Melbourne" in driver.title
elem = driver.find_element_by_id("usernameInput")
elem.clear()
elem.send_keys("ccarner")
elem = driver.find_element_by_id("passwordInput")
elem.send_keys("password")
elem.send_keys(Keys.RETURN)

#now at the echo360 page
assert "Home" in driver.title

# need to sleep so whole page loads, otherwise elements not found since loads dynamically
time.sleep(2)

videos = driver.find_elements_by_css_selector(".menu-opener")
#note, equivalent to videos = driver.find_elements_by_class_name("menu-opener")

print("Located {} videos".format(len(videos)))
if skipVideos != 1:
    print ("Skipping {} videos".format(skipVideos))

print("Downloading videos:")
for (videoNum,video) in enumerate(videos,1):
    if videoNum > skipVideos:
        #don't skip these videos
        video.click()
        time.sleep(1)
        downloadButton = driver.find_element_by_xpath("//*[contains(text(), 'Download original')]")
        downloadButton.click()
        time.sleep(1)
        qualitySelector = driver.find_element_by_class_name('select-wrapper')
        qualitySelector.click()
        time.sleep(1)
        selectionFocus = driver.switch_to.active_element
        selectionFocus.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)
        selectionFocus.send_keys(Keys.RETURN)
        time.sleep(1)
        downloadButton = driver.find_element_by_class_name("downloadBtn")
        downloadButton.click()
        time.sleep(1)
        print(" " + str(videoNum), end ="")
        
print("\nCompleted, downloaded a total of {} videos".format(len(videos)-skipVideos))
quit()

#don't want to close the driver... leave open to ensure downloads continue
#driver.close()