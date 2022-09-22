from os import link
import time
from datetime import datetime
import json
import re
from selenium.webdriver.common.by import By
import re

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
	browser.refresh()
	time.sleep(2)
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

	num_post = browser.find_element(By.CSS_SELECTOR,'ul li:nth-of-type(1) div._aacl:has(span._ac2a)').text
	followers = browser.find_element(By.CSS_SELECTOR,'ul li:nth-of-type(2) div._aacl:has(span._ac2a)').text
	following = browser.find_element(By.CSS_SELECTOR,'ul li:nth-of-type(3) div._aacl:has(span._ac2a)').text

	image = browser.find_element(By.CSS_SELECTOR, 'span._aa8h img').get_attribute('src')
	print('scrapping posts... from user: ', user_scrap)#.append(f'https://www.instagram.com/{name}/?__a=1&__d=dis')
	links = queryGenerator(browser).copy()
	base_url = ['https://www.instagram.com/'+name+'/?__a=1&__d=dis']
	urls_t = base_url + links
	posts = queryCollector(urls_t, browser)
	posts = filter_posts(posts, name)[:50]
	#get the date of the first 50 posts
	print('posts to scrappe',len(posts))#delete shortcode from the url
	for i, post in enumerate(posts):
		print('scrapping date of post: ', i, post['url'])
		date = scrappeDatePost(browser, post['url'])
		posts[i]['date'] = date.split('T')[0]

	dictionary = {'Image': image,'User':name, 'Description': description, 'NoPosts':num_post, 'Followers':followers, 'Following':following, 'Posts': posts, 'Time': now}
	urls_t = []
	links = []
	posts = []
	return dictionary

def scrappeDatePost(browser, url:str) -> str:
	browser.get(url)
	time.sleep(3)
	date = browser.find_element(By.CSS_SELECTOR, 'time._aaqe').get_attribute('datetime')
	return date

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
	logs = []
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
	
	urls = []
	for event in logs:
		url = eventParser(event)
		if url and url not in urls:
			urls.append(url)
	print('urls obtained:', urls)
	return urls

def eventParser(event:dict) -> str:
	text = f'{event}'
	if '?query_hash=' in text and not 'rsrc.php' in text and not 'shortcode' in text:
		print('graphql found')
		url = re.findall(r'"url".*?},', text)
		if len(url) > 0:
			url = url[0].replace('"url":', '').replace('"},', '').replace('"', '')
			return url
	
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
		owner = post['owner']['username']
		post_processed.append({
			'type': type_,
			'url': url,
			'display': display,
			'description': description,
			'comments_count': comments_count,
			'likes_count': likes_count,
			'owner': owner
		})
	print('posts processed: ', len(post_processed))
	return post_processed

def queryCollector(urls:list, browser) -> dict:
	total_posts = []
	print('urls query: ', len(urls), type(urls))
	for url in urls:
		browser.get(url)
		time.sleep(2)
		code = browser.page_source
		jsn = re.findall(r'\{.*\}', code)
		
		if len(jsn) > 0:
			jsn = jsn[0]
		else:
			pass

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
		if 'edge_owner_to_timeline_media' in f'{data}':
			posts = data['edge_owner_to_timeline_media']['edges']
			total_posts += postsParser(posts)
		else:
			print('no posts found in: ', url[:30], '...')
	return total_posts.copy()

def filter_posts(posts, owner):
	unique_posts = []
	# filter repeated posts given the url
	for post in posts:
		if post['url'] not in [p['url'] for p in unique_posts]:
			if post['owner'] == owner:
				unique_posts.append(post)
				
	return unique_posts
