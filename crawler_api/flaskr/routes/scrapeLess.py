from crawler_api.utils.scrapper.scrapper import scrapper
from crawler_api.utils.preprocessing import changeDataType
from crawler_api.flaskr.db import insertDoc, findUser, updateUser

def scrapeLess(username, browser):

  user_data = findUser(username)
  if user_data:
    user_data = scrapper(username, browser)
    user_data = changeDataType(user_data)
    updateUser(username, user_data)
  else:
    user_data = scrapper(username, browser)
    user_data = changeDataType(user_data)
    insertDoc(user_data)