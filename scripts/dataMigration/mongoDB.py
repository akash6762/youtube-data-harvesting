from pymongo import MongoClient
from scripts import makeVideoDetailsAndComments

client = MongoClient("mongodb://localhost:27017")
database = client["youtubeData"]
collection = database["videoData"]

def pushToMongodb(channelName: str):
    data = makeVideoDetailsAndComments(channelName)
    result = collection.insert_one(data)
    client.close()

def retriveFromMongodb():
    pass