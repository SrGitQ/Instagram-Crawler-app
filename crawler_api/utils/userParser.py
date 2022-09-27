'''
get the user from the database and return it with postprocess
'''

import pandas as pd
import warnings
warnings.simplefilter("ignore")
import operator
import re
from cleantext import clean
import datetime
from sklearn.linear_model import LinearRegression
import numpy as np
from statistics import mode
import json
from textblob import TextBlob

import plotly.express as px



def total_likes(data):
    
    likes=[]
    for like in data['posts']:
        likes.append(like['likes'])
        
    total_likes= sum(likes)
    return total_likes


def total_comments(data):
    
    comments=[]
    for com in data['posts']:
        comments.append(com['comments_count'])
        
    total_comments= sum(comments)
    return total_comments

def post_ranking(data):
    
    followers= data['followers']
    query= data['posts'].copy()
    elements=["type", 'description', 'comments_count', 'owner', 'date']
    for x in query:
        percent= round((x['likes'] * 100)/ followers)
        x['scopePercent']= percent
        
        #for item in elements:
        #    del x[item]
        
        
    query.sort(key=operator.itemgetter('likes'), reverse=True)
    return query


def clean_dates(train):
    days=[]
    days_d=[]
    for item in train['date']: ##2016-05-16
        ##print(item)
        day= datetime.datetime.strptime(str(item), '%Y-%m-%d').strftime('%a')
        day_decimal= datetime.datetime.strptime(str(item), '%Y-%m-%d').strftime('%w')
        days.append(day)
        days_d.append(day_decimal)
        
    return days, days_d


def predictor (data):
    
    res= data['posts']
        
    table = []
    for post in res:
        labels = [post['likes'], post['date']]
        table.append(labels)
        
    dataframe= pd.DataFrame()
    train= dataframe.append(table)
    train.columns= ['likes', 'date']

    day, day_decimal= clean_dates(train)
    train= train.assign(day=day, day_decimal=day_decimal )
    #train.drop(['date','type', 'url', 'display', 'description', 'owner', 'scopePercent'], inplace=True, axis=1)
    
    model = LinearRegression()

    x= train['day_decimal'].array.reshape(-1, 1)
    y= train['likes'].array.reshape(-1, 1)
    
    model = LinearRegression().fit(x, y)
    
    ##Predict
    x_new = np.arange(7).reshape((-1, 1)) #days of the week
    y_new = model.predict(x_new)
    general_prediction= round(np.max(y_new))
    return general_prediction


def sentiment(data):

    string=[]
    for item in data['posts']:
        text= item['caption']
        new= clean(text, no_emoji=True)
        new= new.splitlines()
        string.append(new)
    
    element= ['[]']
    for i in string:
        if i== element:
            string.remove(i)
    
    res = [ele for ele in string if ele != []]
    
    sentiment=[]
    for item in res:
        #print(item[0])
        try: 
            text = TextBlob(item[0])
            trans= text.translate(from_lang='es', to='en')
            scores=trans.sentiment.polarity
            #print(scores)

            if scores > 0:
                sentiment.append('Happy person')
            elif scores == 0:
                 sentiment.append('Neutral person')
            elif scores < 0:
                 sentiment.append('Negative person')
        except:
            pass
    general_sentiment= mode(sentiment)
    return general_sentiment


def score(data):

    range1 = range(1000, 9999)
    range2 = range(10000, 99999)
    range3 = range(100000,999999 )
    range4 = range(1000000,10000000000)

    if data['followers'] in range4:
        score = 100
        s =  data['followers'] / 1000000
        print('Celebridad')
    elif data['followers'] in range3: 
        score = 80
        s =  data['followers'] / 100000
        print('Macro influencer')
    elif data['followers'] in range2:
        score = 60
        s = data['followers'] / 10000
        print('Micro Incluencer')
    elif data['followers'] in range1:
        score = 40
        s = data['followers'] / 1000
        print('Nano influencer')
    else: 
        score = 20 
        s = data['followers'] / 100
        print('No influencer')
   
    return score,s




def response(data):
    
    data_fn = {'total_likes': total_likes, 'like_prediction': predictor, 'mood_user': sentiment, 'post_rank': post_ranking, 'score': score}
    for key, fn in data_fn.items():
        try:
            data_fn[key] = fn(data)
        except:
            print('Error calculating {}'.format(key))
            data_fn[key] = None
    #response = {'Total_likes': total_li, 'Likes_prediction': like_prediction, 'Mood_usr': mood_user, 'Post_ranking': post_rank, 'User Score': scoreI}
    
    return data_fn #response

'''
st.session_state['user'] = {
        'username': 'upymemes',
        'img': 'http://localhost:5000/static/jmbalanzar/jmbalanzar.png',
        'bio': 'Instagram is a simple way to capture and share the world’s moments.',
        'no_posts': 0,
        'followers': 0,
        'following': 0,
        'posts': [{"type":"GraphImage","url":"https://www.instagram.com/p/Cf0CiM7l3Jg","display":__img,"description":"Tienes 10 segundos para decirnos lo que sabes, break that one now.","comments_count":1,"likes_count":14,"owner":"jmbalanzar","date":"2022-07-10","scopePercent":11},{"type":"GraphVideo","url":"https://www.instagram.com/p/BizYJ2hBTnc","display":__img,"description":"Good morning! 👌","comments_count":1,"likes_count":12,"owner":"jmbalanzar","date":"2018-05-15","scopePercent":10},{"type":"GraphImage","url":"https://www.instagram.com/p/Bif_dwqh1t8","display":__img,"description":[],"comments_count":1,"likes_count":9,"owner":"jmbalanzar","date":"2018-05-08","scopePercent":7},{"type":"GraphImage","url":"https://www.instagram.com/p/BFc_fohinov","display":__img,"description":[],"comments_count":0,"likes_count":30,"owner":"jmbalanzar","date":"2016-05-16","scopePercent":24}],
        'analitics': {
            'total_likes': 0,
            'total_comms': 0,
            'mood_user': 0,
            'score': [0],
            'post_rank': [{"type":"GraphImage","url":"https://www.instagram.com/p/Bks6dVkjWMW","display":'http://localhost:5000/static/upymemes/posts/Bks6dVkjWMW.png',"description":"Tienes 10 segundos para decirnos lo que sabes, break that one now.","comments_count":1,"likes_count":14,"owner":"jmbalanzar","date":"2022-07-10","scopePercent":11},{"type":"GraphVideo","url":"https://www.instagram.com/p/BktGBeXBLHR","display":'http://localhost:5000/static/upymemes/posts/BktGBeXBLHR.png',"description":"Good morning! 👌","comments_count":1,"likes_count":12,"owner":"jmbalanzar","date":"2018-05-15","scopePercent":10}]
        }
    }

'''
