from pydoc import describe
import streamlit as st
from frontutils.queryd import getUserInfo
from atoms.bar import navbar
from atoms.userInfo import profile_info
from atoms.polbullet import statsBullet
from atoms.posts import postsIcons
from atoms.posts import topPosts
import numpy as np
import pandas as pd


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
</style>""", unsafe_allow_html=True)

#open image

__img = "https://ichef.bbci.co.uk/news/976/cpsprodpb/17638/production/_124800859_gettyimages-817514614.jpg.webp"

if 'user' not in st.session_state:
    st.session_state['user'] = {
        'User': 'upymemes',
        'Image': 'http://localhost:5000/static/upymemes/upymemes.png',
        'Description': 'Instagram is a simple way to capture and share the world’s moments.',
        'NoPosts': 0,
        'Followers': 0,
        'Following': 0,
        'Posts': [{"type":"GraphImage","url":"https://www.instagram.com/p/Cf0CiM7l3Jg","display":__img,"description":"Tienes 10 segundos para decirnos lo que sabes, break that one now.","comments_count":1,"likes_count":14,"owner":"jmbalanzar","date":"2022-07-10","scopePercent":11},{"type":"GraphVideo","url":"https://www.instagram.com/p/BizYJ2hBTnc","display":__img,"description":"Good morning! 👌","comments_count":1,"likes_count":12,"owner":"jmbalanzar","date":"2018-05-15","scopePercent":10},{"type":"GraphImage","url":"https://www.instagram.com/p/Bif_dwqh1t8","display":__img,"description":[],"comments_count":1,"likes_count":9,"owner":"jmbalanzar","date":"2018-05-08","scopePercent":7},{"type":"GraphImage","url":"https://www.instagram.com/p/BFc_fohinov","display":__img,"description":[],"comments_count":0,"likes_count":30,"owner":"jmbalanzar","date":"2016-05-16","scopePercent":24}],
        'analitics': {
            'Total_likes': 0,
            'total_comms': 0,
            'Mood_usr': 0,
            'User Score': [0],
            'Post_ranking': [{"type":"GraphImage","url":"https://www.instagram.com/p/Bks6dVkjWMW","display":'http://localhost:5000/static/upymemes/posts/Bks6dVkjWMW.png',"description":"Tienes 10 segundos para decirnos lo que sabes, break that one now.","comments_count":1,"likes_count":14,"owner":"jmbalanzar","date":"2022-07-10","scopePercent":11},{"type":"GraphVideo","url":"https://www.instagram.com/p/BktGBeXBLHR","display":'http://localhost:5000/static/upymemes/posts/BktGBeXBLHR.png',"description":"Good morning! 👌","comments_count":1,"likes_count":12,"owner":"jmbalanzar","date":"2018-05-15","scopePercent":10}]
        }
    }

#navbar
search_value = navbar()
st.markdown('<br>', unsafe_allow_html=True)

def renderUser(user):
  row1, row2, row3 = st.empty(), st.empty(), st.empty()
  profile_pic = f'http://localhost:5000/static/{user["User"]}/{user["User"]}.png'
  #row 1 divided in 2 columns
  r1_col1, r1_col2 = row1.columns([1,1])
  r1_col1.markdown(profile_info({'User':user['User'], 'Image':profile_pic, 'Posts':user['NoPosts'], 'Followers':user['Followers'], 'Following':user['Following'], 'Description':user['Description']})+'<br>', unsafe_allow_html=True)
  
  table_likes = []
  table_date = []
  url =[]
  for post in user['Posts']:
    table_likes.append(post['likes_count'])
    table_date.append(post['date'])

  table = {'Date': table_date, 'Likes': table_likes}
  
  #r1_col2.markdown(f"<div class='box'></div>", unsafe_allow_html=True)
  #chart_data = pd.DataFrame({'Date': table_date})
  #r1_col2.write(chart_data)
  #st.bar_chart(chart_data['Date'])
  df = pd.DataFrame(
    np.random.randn(15, 1),
    columns=["a"])

  r1_col2.bar_chart(df)

  analitics = user['analitics']

  #row 2 divided in 4 columns
  r2_col1, r2_col2, r2_col3, r2_col4 = row2.columns([1,1,1,1])
  r2_col1.markdown(statsBullet('Total likes', analitics['Total_likes']), unsafe_allow_html=True)
  r2_col2.markdown(statsBullet('Total comments', analitics['total_comms']), unsafe_allow_html=True)
  r2_col3.markdown(statsBullet('She/he is...', analitics['Mood_usr']), unsafe_allow_html=True)
  r2_col4.markdown(statsBullet('Score', analitics['User Score'][0], extra='style="background-color:#000000"')+'<br>', unsafe_allow_html=True)


  #row 3 divided in 2 columns
  r3_col1, r3_col2 = row3.columns([1,1])


  chart_data = pd.DataFrame(table)
  chart_data = chart_data.rename(columns={'Date':'index'}).set_index('index').iloc[::-1, :]
  r3_col1.line_chart(chart_data)

  posts_to_render = []
  for i, post in enumerate(analitics['Post_ranking']):
    shortcode = post['url'].split('/')[-1]
    display = f'http://localhost:5000/static/{user["User"]}/posts/{shortcode}.png'
    analitics['Post_ranking'][i]['display'] = display
  r3_col2.markdown(f"<div class='box' overflow-y: auto; ><div style=' text-align:center'><strong>Post Ranking</strong>{postsIcons()}</div>{topPosts(analitics['Post_ranking'])}</div>", unsafe_allow_html=True)


place = st.empty()
with place.container():
  renderUser(st.session_state['user'])



if search_value:
  place.empty()
  user = getUserInfo(search_value)
  with place.container():
    renderUser(user)
