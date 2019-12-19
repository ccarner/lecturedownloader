"""
Script for downloading lectures from an echo360 page
Made in august 2019 + updated in december 2019.

See readme or use -h flag for more information
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import time
import os 
import argparse

"""========================ARGUMENTS======================================="""
parser = argparse.ArgumentParser()

#positional, required args first
parser.add_argument('url', type=str, help="Url of echo360 lecture page")
parser.add_argument('echo360Email',  type=str, help='email used to log into echo360, need to make an echo360 account and link to unimelb')
parser.add_argument('uomUsername', type=str, help="Unimelb SSO username")
parser.add_argument('uomPassword', type=str, help="Unimelb SSO password")

#now the optional flags
parser.add_argument('-d', metavar="downloadLocation", dest='downloadLocation', default="downloadedLectures", type=str, help="location to save lectures (relative to download folder)" )
parser.add_argument('-w', metavar="waitTime", dest='waitTime', default=3, type=int, help="time to wait in seconds between actions (default 3s, make longer for slower connections)")
parser.add_argument('-s', metavar="skipNum", dest='skipNum', default=0, type=int, help="number of lectures to skip(default 0, use if script previously completed partially to skip the first 's' lectures)")

args = parser.parse_args()


"""========================Webdriver======================================="""
chromeOptions = webdriver.ChromeOptions()
#setting up location for custom download folder if specified
prefs = {"download.default_directory" : "C:\\Users\\colto\\Downloads\\"+ args.downloadLocation}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome( options=chromeOptions)

print("Initialised driver")


"""======================== Navigate to page + Login ======================================="""
driver.get(args.url)

#login page
assert "Email" in driver.title
print ("Arrived at echo360 email page")
elem = driver.find_element_by_id("email")
elem.clear()
elem.send_keys(args.echo360Email)
elem.send_keys(Keys.RETURN)

# need to sleep so whole page loads, otherwise elements not found since loads dynamically
time.sleep(args.waitTime)

#unimelb sso page
assert "Melbourne" in driver.title
print("Arrived at unimelb SSO page")
elem = driver.find_element_by_id("usernameInput")
elem.clear()
elem.send_keys(args.uomUsername)
elem = driver.find_element_by_id("passwordInput")
elem.send_keys(args.uomPassword)
elem.send_keys(Keys.RETURN)

time.sleep(args.waitTime)

#now at the echo360 page
assert "Home" in driver.title
print("Arrived at Echo360 lecture recording page")

time.sleep(args.waitTime)

"""========================Downloading Videos======================================="""

videos = driver.find_elements_by_css_selector(".menu-opener")
#note, equivalent to videos = driver.find_elements_by_class_name("menu-opener")

print("Located {} videos".format(len(videos)))
if args.skipNum != 0:
    print ("Skipping {} videos".format(args.skipNum))

print("Downloading videos:")
for (videoNum,video) in enumerate(videos,1):
    if videoNum > args.skipNum:
        #don't skip these videos
        video.click()
        time.sleep(args.waitTime)
        downloadButton = driver.find_element_by_xpath("//*[contains(text(), 'Download original')]")
        downloadButton.click()
        time.sleep(args.waitTime)
        qualitySelector = driver.find_element_by_class_name('select-wrapper')
        qualitySelector.click()
        time.sleep(args.waitTime)
        selectionFocus = driver.switch_to.active_element
        selectionFocus.send_keys(Keys.ARROW_DOWN)
        time.sleep(args.waitTime)
        selectionFocus.send_keys(Keys.RETURN)
        time.sleep(args.waitTime)
        downloadButton = driver.find_element_by_class_name("downloadBtn")
        downloadButton.click()
        time.sleep(args.waitTime)
        print(" " + str(videoNum), end ="", flush=True)
    else:
        print ("Skipped video # {}".format(videoNum))
        
print("\nCompleted, downloaded a total of {} videos".format(len(videos)-args.skipNum))
quit()

#don't want to close the driver... leave open to ensure downloads continue
#driver.close()