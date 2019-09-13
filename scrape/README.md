## Requirements:
>Python 3 (64 bit) <br />  
>the package dependencies are in the requirements.txt file

# Instructions on how to run the twitter scrape

### Format for how the execution should be ran
`python scrapetweets.py --from_date YYYY-MM-DD --to_date YYYY-MM-DD [HASHTAGS (space separated without '#')]`

### Example
`python scrapetweets.py --from_date 2018-01-01 --to-date 2019-01-01 J35 Orcas`
> This will provide the tweets that include both hastags j35 and orcas from the time period of january 1 2018 to january 1 2019

### This is shorthand for the flags and also works
`python scrapetweets.py -F YYYY-MM-DD -T YYYY-MM-DD [HASHTAGS (space separated without '#')]`

### Example
`python scrapetweets.py -F 2018-01-01 -T 2019-01-01 J35 Orcas`

### Both date flags do not have to be specified. If only the from-date flag is set it will look for tweets from that to present. If only the to-date flag is set it will look for tweets up to that date
`python scrapetweets.py --from_date YYYY-MM-DD [HASHTAGS (space separated without '#')]`
`python scrapetweets.py --to_date YYYY-MM-DD [HASHTAGS (space separated without '#')]`

### Example
`python scrapetweets.py --from_date 2018-01-01 J35 Orcas`
`python scrapetweets.py --to_date 2018-01-01 J35 Orcas`

### The date parameters are optional, if no dates are specified it will run indefinitely until the tweets no longer load
`python scrapetweets.py [HASHTAGS (space separated without '#')]`

### Example
`python scrapetweets.py J35 Orcas`

## List of Features
- Scrapes Tweets based on user inputted tags <br />
- Scrapes Tweets based on user inputted dates <br />
- Places Tweets into excel file in same column <br />

## Set up instructions coming soon
