import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import json

#Este es el Json de prueba que mandó Osiris
doc = open('nuevojson.json')
user_dic = json.load(doc)

doc1 = open('scrapper.json')
u_dict2 = json.load(doc1)


def main():


    col1, col2= st.columns(2) #DEfinir las columnas

    username = "@" + u_dict2['User'] # juntar el arroba con el username desde el json
    

    with col1: #La primer columna donde sale la imagen y la description
        user_description = u_dict2['Description'] #Aquí deber ir la description del usuario
        image = Image.open('Cristiano_Ronaldo_2018.jpg') #Aquí debe ir la imagen del Usuario
        st.header('Instagram Profile')
        st.image(image)
        st.write(user_description)

        
            
        
    with col2:#La columna 2 donde sale toda la información

        
        
        tab1, tab2, tab3 = st.tabs(["Basic info", "Timeline", "Posts Raking"])

        with tab1:
            st.header(username)
            with st.container():

                        
                    user_status = user_dic['Mood_usr']
                    with st.expander("What is The user's Mood?😊😒😐"):
                        st.write(user_status)
                        st.markdown("*The feeling that user has based on the descriptions of all their posts*")

                    likes = user_dic['Total_likes'] #Aquí se sacan los total likes del json

                    prediction = user_dic['Likes_prediction']
                    
                    st.markdown("<h5 style='padding: 3px;font-family: Tahoma, sans-serif; background-color: rgb(105,59,179); background:linear-gradient(153deg, rgba(105,59,179,1) 3%, rgba(128,42,137,1) 21%, rgba(201,5,5,1) 64%, rgba(252,176,69,1) 100%);; opacity:0.9; color: white; border-radius: 5px; border-style: outset'><center> Likes and Likes prediction<center></h5><br>", unsafe_allow_html=True)
                    st.metric("Total of likes this user has got", likes, prediction)

                    comments = user_dic['total_comms'] #De aquí se saca el total de likes 

                    st.markdown("<h5 style='padding: 3px;font-family: Tahoma, sans-serif; background-color: rgb(105,59,179); background:linear-gradient(153deg, rgba(105,59,179,1) 3%, rgba(128,42,137,1) 21%, rgba(201,5,5,1) 64%, rgba(252,176,69,1) 100%);; opacity:0.9; color: white; border-radius: 5px; border-style: outset'><center> Total Comments<center></h5><br>", unsafe_allow_html=True)
                    st.metric("Total of Comments", comments)

                    followers = u_dict2['Followers'] #Aquí deben ir los followers 

                    st.markdown("<h5 style='padding: 3px;font-family: Tahoma, sans-serif; background-color: rgb(105,59,179); background:linear-gradient(153deg, rgba(105,59,179,1) 3%, rgba(128,42,137,1) 21%, rgba(201,5,5,1) 64%, rgba(252,176,69,1) 100%); opacity:0.9; color: white; border-radius: 5px; border-style: outset'><center> Followers <center></h5><br>", unsafe_allow_html=True)
                    st.metric("People who follows this user", followers)

                    following = u_dict2['Following'] #Aquí deben ir la personas que le hacen el follow

                    st.markdown("<h5 style='padding: 3px;font-family: Tahoma, sans-serif; background-color: rgb(105,59,179); background:linear-gradient(153deg, rgba(105,59,179,1) 3%, rgba(128,42,137,1) 21%, rgba(201,5,5,1) 64%, rgba(252,176,69,1) 100%);; opacity:0.9; color: white; border-radius: 5px; border-style: outset'><center> Following <center></h5><br>", unsafe_allow_html=True)
                    st.metric("People who this user follows", following)

                    posts = u_dict2['NoPosts'] #Aquí deben ir los posts

                    st.markdown("<h5 style='padding: 3px;font-family: Tahoma, sans-serif; background-color: rgb(105,59,179); background:linear-gradient(153deg, rgba(105,59,179,1) 3%, rgba(128,42,137,1) 21%, rgba(201,5,5,1) 64%, rgba(252,176,69,1) 100%);; opacity:0.9; color: white; border-radius: 5px; border-style: outset'><center> Posts <center></h5><br>", unsafe_allow_html=True)
                    st.metric("Number of posts", posts)



        with tab2: #Aquí debería ir la línea del tiempo pero no la tengo D: 
            st.header("Timeline")
            df = pd.DataFrame(
            np.random.randn(10, 5),
            columns=('col %d' % i for i in range(5)))

            st.table(df)
            

        with tab3:
            st.header("Post Ranking")
            st.markdown("*Based on the Scope Percent*")

            #Aquí tal vez habría que implementar un if en caso de que no haya publicaciones o que haya menos de 3

            image1 = user_dic['Posr_ranking'][0]['url']
            image2 = "https://s1.eestatic.com/2018/06/25/deportes/futbol/mundial/mundial_de_futbol-mundial_futbol_2018-futbol_317735053_83951015_1706x960.jpg" 
            image3 = "https://assets.goal.com/v3/assets/bltcc7a7ffd2fbf71f5/blt83f0e5e1ae1936a8/62b82d2920b60f0ef7c3b6d6/Cristiano_Ronaldo.jpg?quality=80&format=pjpg&auto=webp&width=1000"

            #Aquí se sacan los likes del json

            likes1 = user_dic['Posr_ranking'][0]['likes_count']
            likes2 = user_dic['Posr_ranking'][1]['likes_count']
            likes3 = user_dic['Posr_ranking'][2]['likes_count']

            #El scope score del json

            scope1 = user_dic['Posr_ranking'][0]['scopePercent']
            scope2 = user_dic['Posr_ranking'][1]['scopePercent']
            scope3 = user_dic['Posr_ranking'][2]['scopePercent']

            with st.container(): #Post Ranking 1 
                st.image(image1)

                with st.expander("#1"):
                        st.write("Likes", likes1)
                        st.write("Scope Percent", scope1)

            with st.container(): #Post Ranking 2
                st.image(image2)

                with st.expander("#2"):
                        st.write("Likes", likes2)
                        st.write("Scope Percent", scope2)

            with st.container(): #Post Ranking 3
                st.image(image3)

                with st.expander("#3"):
                        st.write("Likes", likes3)
                        st.write("Scope Percent", scope3)









    
    
    

    

if __name__ == '__main__':
    main()