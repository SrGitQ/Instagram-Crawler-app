from flask import Flask
from crawler_api.utils.scrapper.browser import InstagramWindow
from crawler_api.utils.credentials import accounts

app = Flask(__name__)

# creating browsers for each account
browsers = [InstagramWindow('/chromedriver', account).browser for account in accounts]

browser_index = 0
current_query_number = 0

def make_query():
  global browser_index
  global current_query_number
  global browsers
  current_query_number += 1
  if current_query_number > 3:
    current_query_number = 0
    browser_index += 1
    if browser_index >= len(browsers):
      browser_index = 0
      browsers = [InstagramWindow('/chromedriver', account).browser for account in accounts]
  print('scrapping with browser: ', browser_index, 'account assigned: ', accounts[browser_index])
  return browsers[browser_index]

#browser = InstagramWindow('/chromedriver').browser

#routes
from .routes.home import home
from .routes.user import user
from .routes.scrapeLess import scrapeLess
from bson.json_util import dumps

@app.route("/")
def root():
  '''
  return general json with all the scrapped users
  '''
  return home()

@app.route("/user/<username>")
def getUser(username):
  '''
  return json with user data
  '''
  user_ = user(username, make_query())
  print('type: ', type(user_))
  return dumps(user_)

@app.route("/scrape/<username>")
def scrapeUser(username):
  '''
  return json with user data and run scrapper even if didn't pass 24 hours
  '''
  return scrapeLess(username, make_query())