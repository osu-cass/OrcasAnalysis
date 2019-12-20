from selenium import webdriver
import time
import xlwt
import argparse
import os

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

try:
    chrome_path = str(os.environ.get("CHROME_PATH"))
except:
    print('CHROME_PATH not specified in environment variables')
    exit()
driver = webdriver.Chrome(chrome_path, options=option)

queryurl = "https://twitter.com/search?f=tweets&vertical=default&q="
for hashtag in args.hashtags:
    queryurl += "%23" + hashtag

if args.from_date:
    queryurl += ' since%3A' + args.from_date
if args.to_date:
    queryurl += ' until%3A' + args.to_date

driver.get(queryurl)

while True:

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

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

tweets = driver.find_elements_by_xpath("//p[@class='TweetTextSize  js-tweet-text tweet-text']")



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

driver.close()
