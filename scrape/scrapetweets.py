from selenium import webdriver
import time
import xlwt
import argparse
import os
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--from_date', '-F', help='Enter start date to search tweets in the form YYYY-MM-DD')
parser.add_argument('--to_date', '-T', help='Enter end date to search tweets YYYY-MM-DD')
parser.add_argument('--lang', '-L', help='Enter Lang Code for specific Language(i.e. en, ja, kr)')
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

if args.lang:
    queryurl += 'lang%3A' + args.lang

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

tweets_container = driver.find_elements_by_xpath("//p[@class='TweetTextSize  js-tweet-text tweet-text']")
tweets_time_stamp_container = driver.find_elements_by_xpath("//span[@class='_timestamp js-short-timestamp ']")

subtweet_links_container = driver.find_elements_by_xpath("//div/div[2]/div[3]/div/a[@class='QuoteTweet-link js-nav']")

# for time in tweets_time_stamp_container:
#     # print(time)
#     # print(time.get_attribute('data-time'))
#     print(datetime.datetime.fromtimestamp(int(time.get_attribute('data-time'))))

tweets = []
for tweet, time in zip(tweets_container, tweets_time_stamp_container):
    tweets.append((tweet.text, str(datetime.datetime.fromtimestamp(int(time.get_attribute('data-time'))))))

# print(subtweet_links_container)
subtweets = []
sub_driver = webdriver.Chrome(chrome_path, options=option)
for container in subtweet_links_container:
    sub_driver.get(container.get_attribute("href"))
    subtweet_text_container = sub_driver.find_element_by_xpath("//p[@class='TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text']")
    subtweet_datetime_container = sub_driver.find_element_by_xpath("//span[@class='metadata']/span")
    subtweet_datetime_raw = subtweet_datetime_container.text
    subtweet_datetime = datetime.datetime.strptime(subtweet_datetime_raw, '%I:%M %p - %d %b %Y')
    # print(subtweet_datetime)
    # subtweet_text = subtweet_text_container.text
    subtweets.append((subtweet_text_container.text,str(subtweet_datetime)))

tweets = tweets + subtweets

workbook = xlwt.Workbook()
sheet = workbook.add_sheet('mytweets')

for index, value in enumerate(tweets):
    try:
        sheet.write(index, 0, value[1])
        sheet.write(index, 1, value[0])
    except:
        continue
outputfile = ''
for hashtag in args.hashtags:
    outputfile = outputfile + hashtag
if args.from_date:
    outputfile = outputfile + 'from(' + str(args.from_date) + ')'
else:
    outputfile = outputfile + 'from(beginning)'

if args.to_date:
    outputfile = outputfile + 'to(' + str(args.to_date) + ')'
else:
    outputfile = outputfile + 'to(now)'
outputfile = outputfile + '.xls'
workbook.save(outputfile)

sub_driver.close()
driver.close()
