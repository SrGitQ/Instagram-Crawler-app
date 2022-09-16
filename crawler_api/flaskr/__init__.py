from flask import Flask
from ..utils.scrapper.browser import InstagramWindow

app = Flask(__name__)
browser = InstagramWindow('/chromedriver').browser

#routes
from .routes.home import home
from .routes.user import user
from .routes.scrapeLess import scrapeLess

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
  return user(username, browser)

@app.route("/scrape/<username>")
def scrapeUser(username):
  '''
  return json with user data and run scrapper even if didn't pass 24 hours
  '''
  return scrapeLess(username, browser)