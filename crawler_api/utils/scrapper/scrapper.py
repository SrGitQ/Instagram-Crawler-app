import time
from datetime import datetime
import json
from selenium.webdriver.common.by import By

def get_links(browser):
  time.sleep(2)
  scrolldown = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
  last_count = ''
  current_links = []
  while(last_count != scrolldown):
    links = browser.find_elements(By.CSS_SELECTOR, "article._aayp a")
    time.sleep(2)
    for link in links:
      if link.get_attribute('href') not in current_links:
        current_links.append(link.get_attribute('href'))
    last_count = scrolldown
    time.sleep(2)
    scrolldown = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
  return current_links

def post_status(browser):
  links = get_links(browser)[:5]
  time.sleep(3)
  posts = []
  for link in links:
    time.sleep(2)
    print('scrapping post: ', link)
    browser.get(link)
    time.sleep(2)
    likes = browser.find_element(By.CSS_SELECTOR, 'section._ae5m span:not([class])').get_attribute('textContent')
    posts.append({'Link': link, 'Likes': likes})
    
  return posts

def scrapper(user_scrap, browser):
  now = str(datetime.now())
  browser.get('https://www.instagram.com/' + user_scrap + '/?hl=en')
  time.sleep(2)
  
  try:
    name = browser.find_element('xpath','/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/div[1]/h2').text
  except:
    name = 'Nan'
  
  try:
    description = browser.find_element('xpath','/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/div[1]/div').text
  except:
    description = 'Nan'
  
  time.sleep(2)
  
  num_post = browser.find_element('xpath','/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[1]/div').text
  followers = browser.find_element('xpath','/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a/div').text
  following = browser.find_element('xpath','/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[3]/a/div').text
  
  image = browser.find_element(By.CSS_SELECTOR, 'span._aa8h img').get_attribute('src')
  print('scrapping posts... from user: ', user_scrap)
  post = post_status(browser)
  dictionary = {'Image': image,'User':name, 'Description': description, 'No Posts':num_post, 'Followers':followers, 'Following':following, 'Posts': post, 'Time': now}
  jsonString = json.dumps(dictionary, indent= 2)
  print('scrapping done', jsonString)
  return jsonString
