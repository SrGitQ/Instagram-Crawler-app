#!/usr/bin/env python
# coding: utf-8

# In[17]:


import pymongo
import json


# In[32]:


#Connnecting to the cluster
myclient = pymongo.MongoClient('mongodb+srv://gabriel:gabo@cluster0.9vebe.mongodb.net/?retryWrites=true&w=majority')
myclient.test


# In[33]:


mydb = myclient['instagramScrapper_DB'] #connecting to the DB


# In[34]:


mycol = mydb['Users'] #connecting to the collection


# In[35]:


def Insert_DB(doc, mycol):  #Function to insert a document into db
    """
    This function inserts a document into the collection Users in the DB
    
    input: 
        doc: This is a dictionary from the JSON got with the scrapper
        mycol: this is the collection where we store the doc
        
    output:
        new_doc: it creates a new doc in the collection
    
    """
    
    new_doc = mycol.insert_one(doc)


# In[48]:


def find_user(username): #Function to find a user given the username, username needs to be a string.
    
    """
    This function finds a user with the string of the username
    
    Input:
        username: A string with the username to seek
        
    Output: 
    
        document: It shows the document from Mongo
    
    """
    
    
    for document in mycol.find({'User': username}):
        print(document)
        print(type(document))
        return document
    


# In[46]:


def update_user(username, data):
    
    """
    
    This is a function to modify a document in the collection given the username 
    
    Input:
        username: A string with the username to seek
        data: This is a dictionary from the JSON with the new information of the user. 
        
    Output: 
    
        mycol.update_one : This is a command that updates one document given the username 
    
    """
    
    myquery = {"User": {"$eq":username}}
    
    new_values = {'$set': data}
    
    mycol.update_one(myquery, new_values)
    
    


# In[37]:


#This should be done in the processing stage 
# It transform the JSON into a dictionary
# Made for testing the functions 


#doc = open('sample.json')
#data = json.load(doc)
#data


# In[38]:


#Insert_DB(data, mycol) #it worked


# In[50]:


# user = find_user('osiris_css') #it worked


# In[47]:


# update_user('osiris_css', data) #it worked 


# In[ ]:




