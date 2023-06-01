from getChannelId import getChannelIdByName
from getPlaylistId import getPlaylistId
from getVideoIds import getVideoIds
from getVideoDetails import getVideoDetails
import json
from config import YOUTUBE


def makeChannelDetails(channelName):
    """

    Parameters
    ----------
    channelName: name of the channel, type:str

    Returns: details of the given YouTube channel in json format
    -------

    """

    channelId = getChannelIdByName(channelName) # channel id
    playlistId = getPlaylistId(channelId) # playlist id

    request = YOUTUBE.channels().list(
        id=channelId,
        part="snippet, statistics"
    )
    response = request.execute()
    channel_name = {
        "channel_name": response["items"][0]["snippet"]["title"],
        "channel_id": response["items"][0]["id"],
        "subscription_count": response["items"][0]["statistics"]["subscriberCount"],
        "channel_views": response["items"][0]["statistics"]["viewCount"],
        "channel_description": response["items"][0]["snippet"]["description"],
        "playlist_id": playlistId
    }

    return channel_name


def extractItemsFromComments(videoId: str):
    """_summary_

    Args:
        videoId (str): unique id of the video

    Returns:
        _type_: details of videos and comments in json
    """
    
    videoDetails = getVideoDetails(videoId)
    if videoDetails["items"][0]["statistics"]["commentCount"] == "0":
        commentCount = 0
        comment = "comments disabled"
        
        return comment, commentCount
    
    else:
        commentCount = videoDetails["items"][0]["statistics"]["commentCount"]
        request = YOUTUBE.commentThreads().list(
            part = "snippet", 
            videoId=videoId,
            textFormat='plainText',
            maxResults=100
        )
        response = request.execute()
        comment = response.get("items", [])
    
    return comment, commentCount
    
    
def makeVideoDetailsAndComments(channelName: str):
    channel_id = getChannelIdByName(channelName)  # channel id
    playlist_id = getPlaylistId(channel_id)  # playlist id
    video_ids = getVideoIds(playlist_id)  # list of all video ids
    
    videoAndCommentsData = []
    for index, video_id in enumerate(video_ids):
        videoInfo = getVideoDetails(video_id)
        
        commentList = [] # the dictionary of comments get appended here
        if ("commentCount" not in videoInfo["items"][0]["statistics"]) or (videoInfo["items"][0]["statistics"]["commentCount"] == "0"):
            commentCount = 0
            comment = "comment disabled"
            commentList.append(comment)
            
        else:
            commentCount = videoInfo["items"][0]["statistics"]["commentCount"]
            commentRequest = YOUTUBE.commentThreads().list(
                part = "snippet", 
                videoId = video_id, 
                textFormat = "plainText", 
                maxResults = 100
            )
            commentResponse = commentRequest.execute()
            
            for number, _id in enumerate(commentResponse):
                commentDictionary = {
                    f"comment_id_{number}": {
                        "comment_id": commentResponse["items"][0]["id"], 
                        "comment_text": commentResponse["items"][0]["snippet"]["topLevelComment"]["snippet"]["textDisplay"], 
                        "comment_author": commentResponse["items"][0]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                        "comment_publishedAt": commentResponse["items"][0]["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                    }
                }
                commentList.append(commentDictionary)
        
        videoDataDictionary = {
            f"video_id_{index}":{
                "video_id": videoInfo["items"][0]["id"],
                "video_name": videoInfo["items"][0]["snippet"]["title"],
                "video_description": videoInfo["items"][0]["snippet"]["description"],
                "publishedAt": videoInfo["items"][0]["snippet"]["publishedAt"],
                "view_count": videoInfo["items"][0]["statistics"]["viewCount"],
                "favorite_count": videoInfo["items"][0]["statistics"]["favoriteCount"],
                "comment_count": commentCount,
                "duration": videoInfo["items"][0]["contentDetails"]["duration"],
                "thumbnail": videoInfo["items"][0]["snippet"]["thumbnails"]["high"]["url"],
                "comments": commentList
        }
            }
        videoAndCommentsData.append(videoDataDictionary)
    
    return videoAndCommentsData
    

def combineData(channelName: str):
    channelDetails = makeChannelDetails(channelName)
    videoDataAndComments = makeVideoDetailsAndComments(channelName)
    
    processedData = {
        "channel_name": channelDetails, 
        "video_and_comments_data": videoDataAndComments
    }

    return processedData

