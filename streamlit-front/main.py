from pydoc import describe
import streamlit as st
from frontutils.queryd import getUserInfo
from atoms.bar import navbar
from atoms.userInfo import profile_info
from atoms.polbullet import statsBullet
from atoms.posts import postsIcons
from atoms.posts import topPosts
#import datetime
from datetime import datetime
import numpy as np
import pandas as pd

def score_(score):
    if score == 100:
        return 'Celebridad'
    elif score == 80: 
        return 'Macro influencer'
    elif score == 60:
        return 'Micro Incluencer'
    elif score == 20:
        return 'Nano influencer'
    else: 
        return 'No influencer'

#streamlit config
st.set_page_config(layout="wide")
st.markdown("""<style>
* {
  margin: 0;
  padding: 0;
}

.box {
  border: 1px solid #36393f;
  border-radius: 15px;
  padding: 15px;
}
.alt-box {
  border: 1px solid #36393f;
  border-radius: 15px;
  padding: 0px;
}
.valuesLayout{
  display: grid;
  grid-template-columns: 1fr 3fr;
}
.valuesLayout > div {
  padding: 5px;
  grid-column-start: 2;
  grid-column-end: 3;
}
.icons {
  display: grid;
  grid-template-columns: 2.3fr 2fr 1fr;
  padding: 5px;

}
a {
  color: white;
  text-decoration: none;
}
</style>""", unsafe_allow_html=True)

#open image

__img = "https://ichef.bbci.co.uk/news/976/cpsprodpb/17638/production/_124800859_gettyimages-817514614.jpg.webp"

if 'user' not in st.session_state:
    st.session_state['user'] = {
        'username': 'jmbalanzar',
        'img': 'http://localhost:5000/static/jmbalanzar/jmbalanzar.png',
        'bio': 'Instagram is a simple way to capture and share the world’s moments.',
        'no_posts': 0,
        'followers': 0,
        'following': 0,
        'posts': [{"type":"GraphImage","url":"https://www.instagram.com/p/Cf0CiM7l3Jg","display":'http://localhost:5000/static/imgs/jmbalanzar/pics/Cf0CiM7l3Jg.png',"caption":"Tienes 10 segundos para decirnos lo que sabes, break that one now.","comments_count":1,"likes":14,"owner":"jmbalanzar","date":"2022-07-10","scopePercent":11, "shortcode":"Cf0CiM7l3Jg"}],
        'analitics': {
            'total_likes': 0,
            'total_comms': 0,
            'mood_user': 0,
            'score': [0],
            'post_rank': [{"type":"GraphImage","url":"https://www.instagram.com/p/Cf0CiM7l3Jg","display":'http://localhost:5000/static/imgs/jmbalanzar/pics/Cf0CiM7l3Jg.png',"caption":"Tienes 10 segundos para decirnos lo que sabes, break that one now.","comments_count":1,"likes":14,"owner":"jmbalanzar","date":"2022-07-10","scopePercent":11, "shortcode":"Cf0CiM7l3Jg"}]
        }
    }

#navbar
search_value = navbar()
st.markdown('<br>', unsafe_allow_html=True)

def renderUser(user):
  row1, row2, row3 = st.empty(), st.empty(), st.empty()
  profile_pic = f'http://localhost:5000/static/imgs/{user["username"]}/{user["username"]}.png'
  #row 1 divided in 2 columns
  r1_col1, r1_col2 = row1.columns([2,1])
  r1_col1.markdown(profile_info({'username':user['username'], 'img':profile_pic, 'no_posts':user['no_posts'], 'followers':user['followers'], 'following':user['following'], 'bio':user['bio']})+'<br>', unsafe_allow_html=True)
  

  table_likes = []
  table_date = []
  url =[]
  for post in user['posts']:
    table_likes.append(post['likes'])
    table_date.append(post['date'])

  table = {'date': table_date, 'likes': table_likes}
  
  #r1_col2.markdown(f"<div class='box'></div>", unsafe_allow_html=True)
  #chart_data = pd.DataFrame({'Date': table_date})
  #r1_col2.write(chart_data)
  #st.bar_chart(chart_data['Date'])
  #df = pd.DataFrame(
  #  np.random.randn(15, 1),
  #  columns=["a"])
#
  #r1_col2.bar_chart(df)

  chart_data = pd.DataFrame({'date': table_date})
  days= []
  for item in chart_data['date']:
    day= datetime.strptime(str(item), '%Y-%m-%d').strftime('%a')
    days.append(day)
  
  chart_data= chart_data.assign(day=days)
  count_days= chart_data.day.value_counts()

  new_df= pd.DataFrame(count_days).reset_index()
  new_df.columns= ['date', 'posts']
  new_df = new_df.rename(columns={'date':'index'}).set_index('index').iloc[::-1, :]
  #r1_col2.bar_chart(new_df)

  analitics = user['analitics']

  #row 2 divided in 4 columns
  r2_col1, r2_col3, r2_col4 = row2.columns([1,1,1])
  r2_col1.markdown(statsBullet('Total likes', analitics['total_likes']), unsafe_allow_html=True)
  #r2_col2.markdown(statsBullet('Total comments', analitics['total_comms']), unsafe_allow_html=True)
  mood = analitics['mood_user']
  if mood == 'Happy person':
    mood = '<img src="http://localhost:5000/static/happy.png" style="width: 70px; height: 70px; border-radius: 50%; object-fit: cover; display: block;">'
  elif mood == 'Neutral person':
    mood = '<img src="http://localhost:5000/static/neutral.png" style="width: 70px; height: 70px; border-radius: 50%;">'
  else:
    mood = '<img src="http://localhost:5000/static/negative.png" style="width: 70px; height: 70px; border-radius: 50%; object-fit: cover; display: block;">'
  r2_col3.markdown(statsBullet('She/he is...', analitics['mood_user']), unsafe_allow_html=True)

  r2_col4.markdown(statsBullet('Score', score_(analitics['score'][0]), extra='style="background-color:#000000"')+'<br>', unsafe_allow_html=True)


  #row 3 divided in 2 columns
  r3_col1, r3_col2 = row3.columns([2,1])


  chart_data = pd.DataFrame(table)
  chart_data = chart_data.rename(columns={'date':'index'}).set_index('index').iloc[::-1, :]
  r3_col1.markdown('<div style="text-align:center"><strong>Likes per dates</strong></div>', unsafe_allow_html=True)
  r3_col1.line_chart(chart_data)
  
  posts_to_render = []
  for i, post in enumerate(analitics['post_rank']):
    shortcode = post['shortcode']
    display = f'http://localhost:5000/static/imgs/{user["username"]}/pics/{shortcode}.png'
    analitics['post_rank'][i]['display'] = display
  r1_col2.markdown(f"<div class='box' overflow-y: auto; syle='height:450px'><div style=' text-align:center'><strong>Post Ranking</strong>{postsIcons()}</div>{topPosts(analitics['post_rank'])}</div><br>", unsafe_allow_html=True)
  r3_col2.markdown('<div style="text-align:center"><strong >posts per day</strong></div>', unsafe_allow_html=True)
  r3_col2.bar_chart(new_df)



place = st.empty()
with place.container():
  renderUser(st.session_state['user'])



if search_value:
  place.empty()
  user = getUserInfo(search_value.replace('%20', ' '))
  with place.container():
    renderUser(user)
    with st.expander('RAW data'):
      st.write(user)
