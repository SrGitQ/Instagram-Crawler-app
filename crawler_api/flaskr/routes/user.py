# get the user information from the database
# if the date has more than 24 hours, update the data
# if the user does not exist, create it
def user(username):
  return f'<h1>User{username}</h1>'