import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crawler_api.scrapper.navigator_assistant import WActions

def createSession(credentials:any, window):
	'''
	Use the window object to create a session on instagram
	given the credentials
	'''

	window.get('https://www.instagram.com/')
	time.sleep(3)
	
	try:
		#login
		username = WebDriverWait(window, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
		password = WebDriverWait(window, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
		username.clear()
		password.clear()
		username.send_keys(credentials['user'])
		password.send_keys(credentials['pass'])
		WebDriverWait(window, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
	except:
		print('error logging in')
		return False

	#close popups
	time.sleep(2)
	WebDriverWait(window, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
	time.sleep(2)
	WebDriverWait(window, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()

	return True

def scrappeUserProfile(user:str, windowActions:WActions):
	'''
	Scrappe the user calling all the functions
	'''
	# go to user page
	windowActions.window.get('https://www.instagram.com/'+user+'/')
	time.sleep(3)

	# store the profile picture
	windowActions.saveNodeScreenshots('div._aarf img', name=user, path=f'./crawler_api/static/imgs/{user}/')
	
	# get the information
	selectors = {
		"username": 	"h2._aacx",
		"followers": 	"ul li:nth-of-type(2) div._aacl:has(span._ac2a)",
		"no_posts": 	"ul li:nth-of-type(1) div._aacl:has(span._ac2a)",
		"following": 	"ul li:nth-of-type(3) div._aacl:has(span._ac2a)",
		"bio": 			"._aa_c ._aad6._aacu",
	}
	data = windowActions.scrappeData(selectors)
	# scrape the first 6 posts
	firsts_posts = windowActions.scrappeData({"posts": "div._aabd a"}, 'href')

	# scroll down to load all the posts
	windowActions.scrollDown(4)
	# making selectors
	posts = windowActions.scrappeData({"posts": "div._aabd a"}, 'href')

	# joining the posts
	for post in firsts_posts['posts']:
		if post not in posts['posts']:
			posts['posts'].append(post)

	return {**data, **posts}

def parsePosts(userData:dict, windows)->dict:
	'''
	transform posts attribute to a list of post objects.
	all the posts will be scrapped by different windows,
	a set of posts will be scrapped firsts and then another set
	'''
	post_info = {
		"caption": "div._aa06:has(h2) div._a9zs span",
		"location": "div._aaqm a",
		"likes": "section._ae5m a.qi72231t ._aacl>span",
	}
	posts = [{'url':url, 'owner':userData['username'], "shortcode":url.split('/')[-2]} for url in userData['posts']]
	
	#index of the window to use
	window_index = 0
	for i, post in enumerate(posts):
		print('go to the post: ', i)
		if window_index >= len(windows):
			time.sleep(3)
			# go back to the first window and scrapp in order
			st_index = i-(len(windows)-1)
			st_index = st_index if st_index >= 0 else st_index*-1
			#scrape every post for each window and reset
			for j, window in enumerate(windows):
				#get the general post info
				data = window.scrappeData(post_info)
				#get the date
				data['date'] = window.scrappeData({"date": "time._aaqe"}, 'datetime')['date'].split('T')[0]
				index = st_index+j-1
				print(f'scrapping the post: {index} with window: {j}')
				
				#save the post image
				window.saveNodeScreenshots('video._ab1d, div._aagv img', name=posts[index]['shortcode'], path=f'./crawler_api/static/imgs/{post["owner"]}/pics/')
				#save the scrapped data on current post
				posts[index] = {**posts[index], **data}

			window_index = 0
		windows[window_index].window.get(post['url'])
		window_index += 1
	
	#scrap the last posts
	for i, post in enumerate(posts):
		try:
			if post['likes']:
				continue
		except:
			windows[0].window.get(post['url'])
			time.sleep(3)
			data = windows[0].scrappeData(post_info)
			data['date'] = windows[0].scrappeData({"date": "time._aaqe"}, 'datetime')['date'].split('T')[0]
			windows[0].saveNodeScreenshots('div._aagv img', name=post['shortcode'], path=f'./crawler_api/static/imgs/{post["owner"]}/pics/')

			posts[i] = {**posts[i], **data}

	userData['posts'] = posts
	return userData

#navigator = WActions()
#navigator_2 = WActions()
#createSession({"user":'karlamakeup14',"pass":'tarea1234'}, navigator.window)
#createSession({"user":'ciscohh1',"pass":'ciscohh3'}, navigator_2.window)
#time.sleep(3)
#data = scrappeUserProfile('', navigator)
#data = parsePosts(data, [navigator, navigator_2])
#print(data)
#navigator.window.close()
#navigator_2.window.close()

#window = WActions(url='https://www.google.com.mx/search?q=perros&hl=en&authuser=0&tbm=isch&sxsrf=ALiCzsa6rFYvQU3FdfFcB-P2k1PjhXgQXw%3A1664138475670&source=hp&biw=1440&bih=796&ei=67wwY8nKJq3LwbkPpsWFkAI&iflsig=AJiK0e8AAAAAYzDK-391OEncbt1NRxp1D1z_FF_X7xsK&ved=0ahUKEwiJ7Mn15rD6AhWtZTABHaZiASIQ4dUDCAc&uact=5&oq=perros&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BAgjECc6CAgAEIAEELEDUABY9QVg2QdoAHAAeACAAW6IAYcFkgEDMC42mAEAoAEBqgELZ3dzLXdpei1pbWc&sclient=img')
#time.sleep(3)
#window.saveNodeScreenshots('img.Q4LuWd', name='perro', path='./imgs/')
#window.scrollDown(2)
#data = window.scrappeData({
#	'imgs': 'img.Q4LuWd'
#}, attr='src')
#print(data)
#window.window.close()



#go to the main page
#scroll down
#scrappe basic data

#use all the browser to get the data
#visit 1 for each one of the 4 accounts
#wait until the page is loaded
#scrappe the data


'''

{
        'username': 'upymemes',
        'img': 'http://localhost:5000/static/jmbalanzar/jmbalanzar.png',
        'bio': 'Instagram is a simple way to capture and share the world’s moments.',
        'no_posts': 0,
        'followers': 0,
        'following': 0,
        'posts': [{"type":"GraphImage","url":"https://www.instagram.com/p/Cf0CiM7l3Jg","display":'http://localhost:5000/static/imgs/jmbalanzar/pics/Cf0CiM7l3Jg.png',"caption":"Tienes 10 segundos para decirnos lo que sabes, break that one now.","comments_count":1,"likes":14,"owner":"jmbalanzar","date":"2022-07-10","scopePercent":11}],
        'analitics': {
            'total_likes': 0,
            'total_comms': 0,
            'mood_user': 0,
            'score': [0],
            'post_rank': [{"type":"GraphImage","url":"https://www.instagram.com/p/Cf0CiM7l3Jg","display":'http://localhost:5000/static/imgs/jmbalanzar/pics/Cf0CiM7l3Jg.png',"caption":"Tienes 10 segundos para decirnos lo que sabes, break that one now.","comments_count":1,"likes":14,"owner":"jmbalanzar","date":"2022-07-10","scopePercent":11}]
        }
    }
'''