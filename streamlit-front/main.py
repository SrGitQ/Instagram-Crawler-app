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


  #row 2 divided in 4 columns
  r2_col1, r2_col2, r2_col3, r2_col4 = row2.columns([1,1,1,1])
  r2_col1.markdown(statsBullet('Total likes', 123), unsafe_allow_html=True)
  r2_col2.markdown(statsBullet('Total comments', 123), unsafe_allow_html=True)
  r2_col3.markdown(statsBullet('She/he is...', 123), unsafe_allow_html=True)
  r2_col4.markdown(statsBullet('Score', 123, extra='style="background-color:#000000"')+'<br>', unsafe_allow_html=True)


  #row 3 divided in 2 columns
  r3_col1, r3_col2 = row3.columns([1,1])

  chart_data = pd.DataFrame(
      np.random.randn(20, 1),
      columns=['a'])
  #example
  r3_col1.area_chart(chart_data)

  r3_col2.markdown(f"<div class='box' overflow-y: auto; ><div style=' text-align:center'><strong>Post Ranking</strong>{postsIcons()}</div>{topPosts([{'img':__img, 'Likes':12,'comments':14}, {'img':__img, 'Likes':12,'comments':14}, {'img':__img, 'Likes':12,'comments':14}, {'img':__img, 'Likes':12,'comments':14}, {'img':__img, 'Likes':12,'comments':14}])}</div>", unsafe_allow_html=True)

place = st.empty()
with place.container():
  renderUser(st.session_state['user'])



if search_value:
  place.empty()
  user = getUserInfo(search_value)
  with place.container():
    renderUser(user)
