import os
import time
from credentials import *
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

class InstagramWindow:
  def __init__(self, driver:str)->None:
    #browser configuration
    route = os.getcwd()
    driver_path = route + driver
    self.browser = webdriver.Chrome(driver_path)
    self.browser.get("https://www.instagram.com/")

    #login
    username = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
    username.clear()
    username.send_keys(user)
    password.clear()
    password.send_keys(pas)
    WebDriverWait(self.browser, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    
    #close popups
    time.sleep(2)
    WebDriverWait(self.browser, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    time.sleep(2)
    WebDriverWait(self.browser, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
