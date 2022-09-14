from datetime import datetime, timedelta
from crawler_api.utils.scrapper.scrapper import scrapper
from crawler_api.utils.preprocessing import changeDataType
from crawler_api.flaskr.db import insertDoc, findUser, updateUser
from crawler_api.utils.timer import isGreater_24hrs

def user(username, browser):
  # check if the user exists in the database
  user_data = findUser(username)
  print(user_data)
  if user_data:
    # check if the user data is older than 24 hours
    if isGreater_24hrs(user_data['Time'], datetime.now()):
      # update the user data and scrape again
      user_data = scrapper(username, browser)
      # preprocess the data
      user_data = changeDataType(user_data)
      # update the user data in the database
      updateUser(username, user_data)
  else:
    #scrape the user
    user_data = scrapper(username, browser)
    # prepare the user data to be saved in the database
    print('scrapped data: ', user_data)
    user_data = changeDataType(user_data)
    # save the user data in the database
    insertDoc(user_data)

  return f'<p>{user_data}</p>'

'''
from datetime import datetime, timedelta

# create datetime now
now = datetime.now()

# create datetime 24 hours ago
ago = now - timedelta(hours=20)

# check if now is greater than 24 hours ago
if now > ago:
  print('now is greater than 24 hours ago')
'''