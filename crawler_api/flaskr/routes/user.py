import datetime
from datetime import timedelta
from crawler_api.utils.scrapper.scrapper import scrapper

def user(username, browser):
  # check if the user exists in the database
  user_data = False
  if user_data:
    # check if the user data is older than 24 hours
    if user_data['date'] < datetime.now() - timedelta(hours=24):
      # update the user data and scrape again
      user_data = 'update_user(username)'
  else:
    #scrape the user
    user_data = scrapper(username, browser)
    # prepare the user data to be saved in the database
    # save the user data in the database

  return f'<p>{user_data}</p>'