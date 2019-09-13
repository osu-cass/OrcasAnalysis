from selenium import webdriver
import time
import xlwt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--from_date', '-F', help='Enter start date to search tweets')
parser.add_argument('--to_date', '-T', help='Enter end date to search tweets')
parser.add_argument('hashtags', nargs='*')
args = parser.parse_args()

option = webdriver.ChromeOptions()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

chrome_path = r"C:\Users\nguyenco\Desktop\chromedriver_win32\chromedriver.exe"

driver = webdriver.Chrome(chrome_path, options=option)

# driver.get("https://twitter.com/search?f=tweets&q=%23j35%23orcas")
queryurl = "https://twitter.com/search?f=tweets&vertical=default&q="
for hashtag in args.hashtags:
    queryurl += "%23" + hashtag

if args.from_date:
    queryurl += ' since%3A' + args.from_date
if args.to_date:
    queryurl += ' until%3A' + args.to_date

driver.get(queryurl)



# print(tweets)
# SCROLL_PAUSE_TIME = 1.0

# Get scroll height
# last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # SCROLL_PAUSE_TIME += .005
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    # time.sleep(SCROLL_PAUSE_TIME)
    try:
        driver.find_element_by_class_name('has-more-items')
    except:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            driver.find_element_by_class_name('has-more-items')
        except:
            break


    # Calculate new scroll height and compare with last scroll height
    # new_height = driver.execute_script("return document.body.scrollHeight")
    # if driver.find_element_by_xpath('//*[@id="timeline"]/div/div[2]/div[1]/div/div[1]/div/p[2]/button'):

    # last_height = new_height

tweets = driver.find_elements_by_xpath("//p[@class='TweetTextSize  js-tweet-text tweet-text']")

driver.close()

workbook = xlwt.Workbook()
sheet = workbook.add_sheet('mytweets')

for index, value in enumerate(tweets):
    try:
        sheet.write(index, 0, value.text)
    except:
        continue
outputfile = '.xls'
for hashtag in args.hashtags:
    outputfile = hashtag + outputfile
workbook.save(outputfile)
