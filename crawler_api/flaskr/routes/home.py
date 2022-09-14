from crawler_api.flaskr.db import findUsers

def home():
  users = findUsers()
  print(users)
  return f"<p>{users}</p>"
