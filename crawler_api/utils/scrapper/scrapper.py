from os import link
import time
from datetime import datetime
from .credentials import *
import json
import re
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
	links = []
	now = str(datetime.now())
	browser.get('https://www.instagram.com/' + user_scrap + '/?hl=en')
	time.sleep(2)
	browser.refresh()
	time.sleep(2)

	try:
		name = browser.find_element(By.CSS_SELECTOR,'h2._aacx').text
	except:
		name = ''

	try:
		description = browser.find_element(By.CSS_SELECTOR,'._aa_c ._aad6._aacu').text
	except:
		description = ''

	time.sleep(2)

	num_post = browser.find_element('xpath','/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[1]/div').text
	followers = browser.find_element('xpath','/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a/div').text
	following = browser.find_element('xpath','/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[3]/a/div').text

	image = browser.find_element(By.CSS_SELECTOR, 'span._aa8h img').get_attribute('src')
	print('scrapping posts... from user: ', user_scrap)#.append(f'https://www.instagram.com/{name}/?__a=1&__d=dis')
	links = queryGenerator(browser).copy()
	base_url = ['https://www.instagram.com/'+name+'/?__a=1&__d=dis']
	links += base_url
	post = queryCollector(links, browser)
	dictionary = {'Image': image,'User':name, 'Description': description, 'NoPosts':num_post, 'Followers':followers, 'Following':following, 'Posts': post, 'Time': now}
	links = []

	return dictionary

def process_browser_logs_for_network_events(logs):
	"""
	Return only logs which have a method that start with "Network.response", "Network.request", or "Network.webSocket"
	since we're interested in the network events specifically.
	"""
	for entry in logs:
		log = json.loads(entry["message"])["message"]
		if (
		    "Network.response" in log["method"]
		    or "Network.request" in log["method"]
		    or "Network.webSocket" in log["method"]
		):    
			yield log

def queryGenerator(browser) -> list:
	time.sleep(2)
	scrolldown = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	last_count = ''	
	while (last_count != scrolldown):
		time.sleep(2)
		last_count= scrolldown
		time.sleep(2)
		scrolldown = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")	
	time.sleep(2)
	logs = browser.get_log("performance")
	urls = [eventParser(event) for event in logs if eventParser(event)]
	print('urls obtained:', urls)
	return urls

def eventParser(event:dict) -> str:
	try:
		if event['message']['params']['response']['url'] != None:
			print(event)
			return event['message']['params']['response']['url']#get if graphql 
	except:
		return False

def postsParser(posts:dict)->list:
	post_processed = []
	#print('given posts: ', len(posts), posts)
	for post in [node['node'] for node in posts]:
		type_ = post['__typename']
		display = post['display_url']
		description = post['edge_media_to_caption']['edges']#[0]['node']['text']
		if len(description) > 0:
			description = description[0]['node']['text']
		comments_count = post['edge_media_to_comment']['count']
		likes_count = post['edge_media_preview_like']['count']
		url = 'https://www.instagram.com/p/' + post['shortcode']
		post_processed.append({
			'type': type_,
			'url': url,
			'display': display,
			'description': description,
			'comments_count': comments_count,
			'likes_count': likes_count
		})
	print('posts processed: ', len(post_processed))
	return post_processed

def queryCollector(urls:list, browser) -> dict:
	total_posts = []
	print('urls query: ', len(urls), urls, type(urls))
	for url in urls:
		browser.get(url)
		time.sleep(2)
		code = browser.page_source
		jsn = re.findall(r'\{.*\}', code)[0]

		try:
			if 'seo_category_infos' in jsn:
				data = json.loads(jsn)['graphql']['user']
				print('getting posts from graphql')
			else:
				data = json.loads(jsn)['data']['user']
				print('graphiql not found')
		except:
			print('error in json')
			continue
		total_posts += postsParser(data['edge_owner_to_timeline_media']['edges'])
	print('total posts: ', len(total_posts), total_posts)
	return total_posts.copy()
