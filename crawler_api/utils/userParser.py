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
    for like in data['Posts']:
        likes.append(like['likes_count'])
        
    total_likes= sum(likes)
    return total_likes


def total_comments(data):
    
    comments=[]
    for com in data['Posts']:
        comments.append(com['comments_count'])
        
    total_comments= sum(comments)
    return total_comments

def post_ranking(data):
    
    followers= data['Followers']
    query= data['Posts']
    elements=["type", 'description', 'comments_count', 'owner', 'date']
    for x in query:
        percent= round((x['likes_count'] * 100)/ followers)
        x['scopePercent']= percent
        
        for item in elements:
            del x[item]
        
        
    query.sort(key=operator.itemgetter('likes_count'), reverse=True)
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
    
    res= data['Posts']
        
    table = []
    for post in res:
        labels = [post['comments_count'],post['likes_count'], post['date']]
        table.append(labels)
        
    dataframe= pd.DataFrame()
    train= dataframe.append(table)
    train.columns= ['comments_count', 'likes_count', 'date']

    day, day_decimal= clean_dates(train)
    train= train.assign(day=day, day_decimal=day_decimal )
    #train.drop(['date','type', 'url', 'display', 'description', 'owner', 'scopePercent'], inplace=True, axis=1)
    
    model = LinearRegression()

    x= train['day_decimal'].array.reshape(-1, 1)
    y= train['likes_count'].array.reshape(-1, 1)
    
    model = LinearRegression().fit(x, y)
    
    ##Predict
    x_new = np.arange(7).reshape((-1, 1)) #days of the week
    y_new = model.predict(x_new)
    general_prediction= round(np.max(y_new))
    return general_prediction


def sentiment(data):

    string=[]
    for item in data['Posts']:
        text= item['description']
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

    if data['Followers'] in range4:
        score = 100
        s =  data['Followers'] / 1000000
        print('Celebridad')
    elif data['Followers'] in range3: 
        score = 80
        s =  data['Followers'] / 100000
        print('Macro influencer')
    elif data['Followers'] in range2:
        score = 60
        s = data['Followers'] / 10000
        print('Micro Incluencer')
    elif data['Followers'] in range1:
        score = 40
        s = data['Followers'] / 1000
        print('Nano influencer')
    else: 
        score = 20 
        s = data['Followers'] / 100
        print('No influencer')
   
    return score,s 




def response(data):
    
    total_li= total_likes(data)
    total_comm= total_comments(data)
    like_prediction= predictor(data)
    mood_user= sentiment(data)
    post_rank= post_ranking(data)
    scoreI = score(data)
    
    response= {'Total_likes': total_li, 'total_comms': total_comm, 'Likes_prediction': like_prediction, 'Mood_usr': mood_user, 'Post_ranking': post_rank, 'User Score': scoreI}
    
    return response
