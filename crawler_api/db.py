import pymongo
import certifi
from crawler_api.credentials import db_url

ca = certifi.where()
myclient = pymongo.MongoClient(db_url, tlsCAFile=ca)

mydb = myclient['instagramScrapper_DB']

mycol = mydb['Users']


def insertDoc(doc):  #Function to insert a document into db
  """
  This function inserts a document into the collection Users in the DB
  
  input: 
    doc: This is a dictionary from the JSON got with the scrapper
      
  output:
    new_doc: it creates a new doc in the collection
  """
  
  new_doc = mycol.insert_one(doc)
  
def findUser(username): #Function to find a user given the username, username needs to be a string.
  
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

def findUsers():
  
  """
  
  This is a function to find all the users in the collection
  
  Input:
    None
      
  Output: 
  
    document: It shows the document from Mongo
  
  """
  
  return [u for u in mycol.find()]

def updateUser(username, data):
  
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
