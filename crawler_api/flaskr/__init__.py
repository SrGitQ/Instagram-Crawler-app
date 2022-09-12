from flask import Flask

app = Flask(__name__)

#routes
from .routes.home import home
from .routes.user import user

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
  return user(username)