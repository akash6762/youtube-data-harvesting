import sys
import os
from pymongo import MongoClient
from youtubeApi.getChannelId import getChannelIdByName

if __name__ == '__main__':
    print(getChannelIdByName("future demand"))


"""client = MongoClient("mongodb://127.0.0.1:27017") # mongo client 
database = client["youtube"] # database
doument = database["statistics"] # document"""
