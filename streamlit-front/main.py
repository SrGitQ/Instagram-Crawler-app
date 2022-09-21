import streamlit as st
import requests
import json

def getUserInfo(username):
  url = "http://localhost:5000/user/" + username
  response = requests.get(url)
  return response.json()

#make a request to the local backend
user_data = getUserInfo('jmbalanzar')
st.write(type(user_data))

user_data