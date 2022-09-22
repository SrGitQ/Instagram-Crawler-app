import requests
import json

def getUserInfo(username):
  url = "http://localhost:5000/user/" + username
  response = requests.get(url)
  return response.json()