import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class WActions:
	def __init__(self, window=None, url:str='')->None:
		'''
		Window actions is a class that helps to scrappe data
		from a browser using selectors as a dictionary and a url
		then it returns the data scrapped from the url with the
		same structure as the selectors.

		Example:
		INPUT: 
			url = 'https://www.instagram.com/instagram/'
			selectors = {
				"username": "div.username",
				"followers": "div.followers",
			}
		OUTPUT:
			{
				"username": "instagram",
				"followers": "100M",
			}
		is highly recommended wait until the page is loaded...
		'''
		self.window = window if window else self.createWindow()
		if url != '':
			self.window.get(url)

	def createWindow(self, driver:str='chromedriver', path=None)->None:
		'''
		Create a browser instance
		'''
		if path is None:
			path = os.getcwd()
		self.window = webdriver.Chrome(service=Service(path+'/'+driver))
		return self.window

	def scrappeData(self, selectors:any, attr:str='textContent')->any:
		def getSelectorData(selector:str, name:str='default')->str:
			'''
			try to get the selector information and return
			an error in case of failure
			'''
			try:
				nodes = self.window.find_elements(By.CSS_SELECTOR, selector)

				# getting the data from the nodes
				items = [node.get_attribute(attr) for node in nodes].copy()
				# filter None values
				items = list(filter(lambda x: x is not None, items))

				# returning the data
				return items if len(items) > 1 else items[0]
			except:
				print('error getting selector: ', selector, 'with name: ', name)
				return ''

		'''
		Scrappe data from the page using the selectors and return
		the data scrapped with the same structure as the selectors.
		'''
		data = {}
		for key in selectors:
			data[key] = getSelectorData(selectors[key], name=key)
		return data
	
	def saveNodeScreenshots(self, selector:str, name:str='default', path:str='./')->None:
		'''
		Take the screenshot of the node given the selector
		path needs to end with '/'
		'''
		try:
			if not os.path.exists(path):
				os.makedirs(path)
			with open(path+name+'.png', 'wb') as file:
				file.write(self.window.find_element(By.CSS_SELECTOR, selector).screenshot_as_png)
		except:
			print('error getting screenshot of the node')
			return

	
	def scrollDown(self, times:int=1)->None:
		'''
		Scroll down the page the times specified
		'''
		for i in range(times):
			self.window.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
			time.sleep(2)
	
	def runFn(self, Fn)->None:
		'''
		Run a query function with the browser
		'''
		return Fn(self.window)
