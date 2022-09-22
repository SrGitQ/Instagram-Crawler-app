from datetime import datetime, timedelta
from crawler_api.utils.scrapper.scrapper import scrapper
from crawler_api.utils.preprocessing import changeDataType
from crawler_api.flaskr.db import insertDoc, findUser, updateUser
from crawler_api.utils.timer import isGreater_24hrs
from crawler_api.utils.preprocessing import preprocess
from crawler_api.utils.userParser import response
from flask import jsonify, make_response
import json

def user(username, browser):
  # check if the user exists in the database
  user_data = findUser(username)
  print('user data already' if user_data else 'user data not found')
  if user_data:
    # check if the user data is older than 24 hours
    date = user_data['Time']#[:19]
    #print('auxiliar:', date)
    if isGreater_24hrs(datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f'), datetime.now()):
      print('user data is older than 24 hours - updating')
      # update the user data and scrape again
      user_data = scrapper(username, browser)
      # preprocess the data
      user_data = preprocess(user_data)

      # analize metrics
      user_data['analitics'] = response(user_data)

      # update the user data in the database
      updateUser(username, user_data)
  else:
    print('scraping user data')
    #scrape the user
    user_data = scrapper(username, browser)

    # prepare the user data to be saved in the database
    print('scrapped data: ', f'{user_data}'[:50], '...')
    user_data = preprocess(user_data)

    # analize metrics
    user_data['analitics'] = response(user_data)

    # save the user data in the database
    insertDoc(user_data)

  return user_data
