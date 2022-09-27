from bson.json_util import dumps
from crawler_api.credentials import accounts
from flask import Flask, send_from_directory
from crawler_api.scrapper.instagram_conf import parsePosts
from crawler_api.scrapper.instagram_conf import createSession
from crawler_api.scrapper.navigator_assistant import WActions
from crawler_api.scrapper.instagram_conf import scrappeUserProfile
from crawler_api.db import findUser, insertDoc, updateUser
from crawler_api.utils.timer import isGreater_24hrs
from crawler_api.utils.preprocessing import preprocess
from crawler_api.utils.userParser import response
from datetime import datetime

windows = [WActions() for account in accounts]
for i, account in enumerate(accounts):
	createSession(account, windows[i].window)

app = Flask(__name__)

@app.route("/static/<path:path>")
def static_dir(path):
	return send_from_directory("./static/imgs", path)

def userFullParsed(username, windows):
	# scrappe the user data
	user_data = scrappeUserProfile(username, windows[0])
	# parse all the posts of the user
	user_data = parsePosts(user_data, windows)
	# update the scrapped_date
	user_data['scrapped_date'] = str(datetime.now())
	# preprocess the data
	user_data = preprocess(user_data)
	#analyze the data
	user_data['analitics'] = response(user_data)
	return user_data

@app.route("/user/<username>")
def getUser(username):
	user_data = findUser(username)
	if user_data:
		date = user_data['scrapped_date']
		if isGreater_24hrs(datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f'), datetime.now()):
			# scrappe the user data
			user_data = userFullParsed(username, windows)
			updateUser(username, user_data)
	else:
		# scrappe the user data
		user_data = userFullParsed(username, windows)
		insertDoc(user_data)
	return dumps(user_data)