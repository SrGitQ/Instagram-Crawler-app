'''
Scrape a instagram user and return a json
'''
from crawler_api.utils.scrapper.credentials import * 
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
from datetime import datetime
import re
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize
import pandas as pd, numpy as np
import os
import wget
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

ruta= os.getcwd()
driver_path= '{}\chromedriver.exe'.format(ruta)
browser= webdriver.Chrome(driver_path)
browser.get("https://www.instagram.com/")

username = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

#enter username and password
username.clear()
username.send_keys(user)
password.clear()
password.send_keys('tarea1234')
#target the login button and click it
button = WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

time.sleep(2)
alert = WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Ahora no")]'))).click()
time.sleep(2)
alert2 = WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Ahora no")]'))).click()

def initialization (user_scrap,browser):
    ##ruta= os.getcwd()
    #driver_path= '{}\chromedriver.exe'.format(ruta)
    #browser= webdriver.Chrome(driver_path)
    
    #time.sleep(2)
    now = str(datetime.now())
    browser.get('https://www.instagram.com/'+user_scrap+'/?hl=en')
    ##Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    ##Name and description
    time.sleep(2)
    
    try:
        name= browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/div[1]/h2').text
        #name= driver.find_element(By.CSS_SELECTOR, 'span._aacl').get_attribute('textContent')
        #print(name)
    except:
        name= 'Nan'
    
    try:
        description= browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div[1]/div').text
        #print(description)
    except:
        description= 'Nan'
    
    ##Numbers of user
    
    time.sleep(2)
    
    num_post = browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[1]/div').text
    #print(num_post)
    #time.sleep(2)
    followers= browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a/div').text
    following= browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[3]/a/div').text
    
    image= browser.find_element(By.CSS_SELECTOR, 'span._aa8h img').get_attribute('src')
 
    #num_post= driver.find_element(By.CSS_SELECTOR, 'section._ae5m span:not([class])').get_attribute('textContent')
    
    
    post= post_status (user_scrap, browser)
    dictionary = {'Image': image,'User':name, 'Description': description, 'No Posts':num_post, 'Followers':followers, 'Following':following, 'Posts': post, 'Time': now}
    jsonString = json.dumps(dictionary, indent= 2)
    return jsonString

def post_status (user_scrap, browser):
    
    browser.get('https://www.instagram.com/'+user_scrap+'/?hl=en')
    
    scrolldown = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    match=False
    while(match==False):
        last_count = scrolldown
        time.sleep(3)
        scrolldown = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        #scrolldown = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        if last_count==scrolldown:
            match=True
    
    posts = []
    links = browser.find_elements_by_tag_name("a")
    

    for link in links:
        post = link.get_attribute('href')
        if '/p/' in post:
            posts.append(post)
    time.sleep(2)
    
    #print(posts)
    

    likes= []
    time.sleep(2)
    
    for post in posts[:10]:
        ##print(post)
        browser.get(post)
        time.sleep(5)
        #name= driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/div/a/div/span').text
        #name= driver.find_element(By.CSS_SELECTOR, 'section._ae5m')
        name= browser.find_element(By.CSS_SELECTOR, 'section._ae5m span:not([class])').get_attribute('textContent')
        
        dictionary= {'Link': post, 'Likes': name}
        likes.append(dictionary)
        
        
    return likes

json1= initialization (user_scrap, browser)

with open("sample.json", "w") as outfile:
    outfile.write(json1)