from bson.json_util import dumps
from crawler_api.credentials import accounts
from flask import Flask, send_from_directory
from crawler_api.scrapper.instagram_conf import parsePosts
from crawler_api.scrapper.instagram_conf import createSession
from crawler_api.scrapper.navigator_assistant import WActions
from crawler_api.scrapper.instagram_conf import scrappeUserProfile
from crawler_api.db import findUser, insertDoc, updateUser
from crawler_api.utils.timer import isGreater_24hrs
from datetime import datetime

windows = [WActions() for account in accounts]
for i, account in enumerate(accounts):
	createSession(account, windows[i])

app = Flask(__name__)

@app.route("/static/<path:path>")
def static_dir(path):
	return send_from_directory("./scrapper/imgs", path)

def userFullParsed(username, windows):
	# scrappe the user data
	user_data = scrappeUserProfile(username, windows[0])
	# parse all the posts of the user
	user_data = parsePosts(user_data, windows)
	# update the scrapped_date
	user_data['scrapped_date'] = datetime.now()
	# preprocess the data

	#analyze the data

	return user_data

@app.route("/user/<username>")
def getUser(username):
	user_data = findUser(username)
	if user_data:
		date = user_data['scrapped_date']
		if isGreater_24hrs(date, datetime.now()):
			# scrappe the user data
			user_data = userFullParsed(username, windows)
			updateUser(username, user_data)
	else:
		# scrappe the user data
		user_data = userFullParsed(username, windows)
		insertDoc(user_data)
	return user_data