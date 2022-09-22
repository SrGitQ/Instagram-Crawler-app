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

if 'user' not in st.session_state:
    st.session_state['user'] = {
        'User': 'instagram',
        'Image': 'https://ichef.bbci.co.uk/news/976/cpsprodpb/17638/production/_124800859_gettyimages-817514614.jpg.webp',
        'Description': 'Instagram is a simple way to capture and share the world’s moments.',
        'NoPosts': 0,
        'Followers': 0,
        'Following': 0,
        'Posts': [{"type":"GraphImage","url":"https://www.instagram.com/p/Cf0CiM7l3Jg","display":"https://instagram.fmid2-1.fna.fbcdn.net/v/t51.2885-15/292520055_5328160093889478_5819946844383595273_n.webp?stp=dst-jpg_e35&amp;_nc_ht=instagram.fmid2-1.fna.fbcdn.net&amp;_nc_cat=106&amp;_nc_ohc=NRoXegHX_RoAX-bWTHl&amp;edm=ABfd0MgBAAAA&amp;ccb=7-5&amp;oh=00_AT_ZKz0f_dWLv9ZFb8fwqhqYPzLeSXKUZTEoKCqoShGhDg&amp;oe=63341C29&amp;_nc_sid=7bff83","description":"Tienes 10 segundos para decirnos lo que sabes, break that one now.","comments_count":1,"likes_count":14,"owner":"jmbalanzar","date":"2022-07-10","scopePercent":11},{"type":"GraphVideo","url":"https://www.instagram.com/p/BizYJ2hBTnc","display":"https://instagram.fmid2-1.fna.fbcdn.net/v/t51.2885-15/32035672_575200616200634_6964604897157185536_n.jpg?stp=dst-jpg_e35&amp;_nc_ht=instagram.fmid2-1.fna.fbcdn.net&amp;_nc_cat=102&amp;_nc_ohc=aIRG-AWD730AX8jxsxX&amp;edm=ABfd0MgBAAAA&amp;ccb=7-5&amp;oh=00_AT_7hf50k9P0n3PG7UrjI6n7_NTJd9wq5qSxffSVqUmaAA&amp;oe=632E934E&amp;_nc_sid=7bff83","description":"Good morning! 👌","comments_count":1,"likes_count":12,"owner":"jmbalanzar","date":"2018-05-15","scopePercent":10},{"type":"GraphImage","url":"https://www.instagram.com/p/Bif_dwqh1t8","display":"https://instagram.fmid2-1.fna.fbcdn.net/v/t51.2885-15/31065389_164633570884044_3160913372271083520_n.jpg?stp=dst-jpg_e35&amp;_nc_ht=instagram.fmid2-1.fna.fbcdn.net&amp;_nc_cat=100&amp;_nc_ohc=qfm0fNwKbdcAX-nvFA_&amp;edm=ABfd0MgBAAAA&amp;ccb=7-5&amp;oh=00_AT_tX6LXSWrJ8SyzIbA8ZLjX7S8H7ZIZIAzbaIAynDYgvA&amp;oe=6333AC46&amp;_nc_sid=7bff83","description":[],"comments_count":1,"likes_count":9,"owner":"jmbalanzar","date":"2018-05-08","scopePercent":7},{"type":"GraphImage","url":"https://www.instagram.com/p/BFc_fohinov","display":"https://instagram.fmid2-1.fna.fbcdn.net/v/t51.2885-15/13166979_952431651521524_724075705_n.jpg?stp=dst-jpg_e35&amp;_nc_ht=instagram.fmid2-1.fna.fbcdn.net&amp;_nc_cat=104&amp;_nc_ohc=SftSNcgI9SkAX_9Nq33&amp;tn=ZloNr8oV5EtLlKw7&amp;edm=ABfd0MgBAAAA&amp;ccb=7-5&amp;oh=00_AT9rTTyrTFj3JeT4GBBMJ3lbdq8jKlkqLc4KfKirvrHZIg&amp;oe=6332C6BB&amp;_nc_sid=7bff83","description":[],"comments_count":0,"likes_count":30,"owner":"jmbalanzar","date":"2016-05-16","scopePercent":24}],
        'analitics': {
            'Total_likes': 0,
            'total_comms': 0,
            'Mood_usr': 0,
            'User Score': [0],
            'Post_ranking': []
        }
    }

#navbar
search_value = navbar()
st.markdown('<br>', unsafe_allow_html=True)
__img = "https://ichef.bbci.co.uk/news/976/cpsprodpb/17638/production/_124800859_gettyimages-817514614.jpg.webp"

def renderUser(user):
  row1, row2, row3 = st.empty(), st.empty(), st.empty()

  #row 1 divided in 2 columns
  r1_col1, r1_col2 = row1.columns([1,1])
  r1_col1.markdown(profile_info({'User':user['User'], 'Image':user['Image'], 'Posts':user['NoPosts'], 'Followers':user['Followers'], 'Following':user['Following'], 'Description':user['Description']})+'<br>', unsafe_allow_html=True)
  r1_col2.markdown(f"<div class='box'></div>", unsafe_allow_html=True)

  analitics = user['analitics']

  #row 2 divided in 4 columns
  r2_col1, r2_col2, r2_col3, r2_col4 = row2.columns([1,1,1,1])
  r2_col1.markdown(statsBullet('Total likes', analitics['Total_likes']), unsafe_allow_html=True)
  r2_col2.markdown(statsBullet('Total comments', analitics['total_comms']), unsafe_allow_html=True)
  r2_col3.markdown(statsBullet('She/he is...', analitics['Mood_usr']), unsafe_allow_html=True)
  r2_col4.markdown(statsBullet('Score', analitics['User Score'][0], extra='style="background-color:#000000"')+'<br>', unsafe_allow_html=True)


  #row 3 divided in 2 columns
  r3_col1, r3_col2 = row3.columns([1,1])

  table_likes = []
  table_date = []
  for post in user['Posts']:
    table_likes.append(post['likes_count'])
    table_date.append(post['date'])
  table = {'Date': table_date, 'Likes': table_likes}

  chart_data = pd.DataFrame(table)
  chart_data = chart_data.rename(columns={'Date':'index'}).set_index('index').iloc[::-1, :]
  r3_col1.line_chart(chart_data)

  r3_col2.markdown(f"<div class='box' overflow-y: auto; ><div style=' text-align:center'><strong>Post Ranking</strong>{postsIcons()}</div>{topPosts(analitics['Post_ranking'])}</div>", unsafe_allow_html=True)


place = st.empty()
with place.container():
  renderUser(st.session_state['user'])



if search_value:
  place.empty()
  user = getUserInfo(search_value)
  with place.container():
    renderUser(user)
    st.write(user)
