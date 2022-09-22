import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

def main():


    col1, col2= st.columns(2)

    with col1:
        image = Image.open('Cristiano_Ronaldo_2018.jpg')
        st.header("@cristiano")
        st.image(image, caption='CR7 GOD Juego para el Real Madrid')

        
    with col2:

        
        tab1, tab2, tab3 = st.tabs(["Basic info", "Timeline", "Posts Raking"])

        with tab1:
            #st.header("Basic Info")
            with st.container():

                    user_status = 'Neutral Person'
                    st.write("Click to see User's Mood")

                    if st.button('Mood User', key='Mood'):
                        st.write(user_status)

                    followers = 10
                    st.markdown("<h5 style='padding: 3px;font-family: Tahoma, sans-serif; background-color: rgb(105,59,179); background:linear-gradient(153deg, rgba(105,59,179,1) 3%, rgba(128,42,137,1) 21%, rgba(201,5,5,1) 64%, rgba(252,176,69,1) 100%); opacity:0.9; color: white; border-radius: 5px; border-style: outset'><center> Followers <center></h5><br>", unsafe_allow_html=True)
                    st.metric("People who follows this user", followers)

                    following = 330
                    st.markdown("<h5 style='padding: 3px;font-family: Tahoma, sans-serif; background-color: rgb(105,59,179); background:linear-gradient(153deg, rgba(105,59,179,1) 3%, rgba(128,42,137,1) 21%, rgba(201,5,5,1) 64%, rgba(252,176,69,1) 100%);; opacity:0.9; color: white; border-radius: 5px; border-style: outset'><center> Following <center></h5><br>", unsafe_allow_html=True)
                    st.metric("People who this user follows", following)

                    posts = 70
                    st.markdown("<h5 style='padding: 3px;font-family: Tahoma, sans-serif; background-color: rgb(105,59,179); background:linear-gradient(153deg, rgba(105,59,179,1) 3%, rgba(128,42,137,1) 21%, rgba(201,5,5,1) 64%, rgba(252,176,69,1) 100%);; opacity:0.9; color: white; border-radius: 5px; border-style: outset'><center> Posts <center></h5><br>", unsafe_allow_html=True)
                    st.metric("Number of posts", posts)

                    likes = 20
                    prediction = 20
                    st.markdown("<h5 style='padding: 3px;font-family: Tahoma, sans-serif; background-color: rgb(105,59,179); background:linear-gradient(153deg, rgba(105,59,179,1) 3%, rgba(128,42,137,1) 21%, rgba(201,5,5,1) 64%, rgba(252,176,69,1) 100%);; opacity:0.9; color: white; border-radius: 5px; border-style: outset'><center> Likes and Likes prediction<center></h5><br>", unsafe_allow_html=True)
                    st.metric("Total of likes this user has got", likes, prediction)

        with tab2:
            st.header("Timeline")
            df = pd.DataFrame(
            np.random.randn(10, 5),
            columns=('col %d' % i for i in range(5)))

            st.table(df)
            

        with tab3:
            st.header("Post Ranking")
            
            st.write("This is inside a tab")

            # You can call any Streamlit command, including custom components:
            st.bar_chart(np.random.randn(50, 3))
            with st.expander("See explanation"):
                    st.write("""
                    The chart above shows some numbers I picked for you.
                    I rolled actual dice for these, so they're *guaranteed* to
                    be random.
                    """)

    








    
    
    

    

if __name__ == '__main__':
    main()