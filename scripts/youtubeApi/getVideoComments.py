from config import YOUTUBE
from getVideoDetails import getVideoDetails


def getComments(videoId):
    """

    Parameters
    ----------
    videoId: video id

    Returns: comments of the video in json format
    -------

    """

    videoDetails = getVideoDetails(videoId)
    if ("commentCount" not in videoDetails["items"][0]["statistics"]) or (videoDetails["items"][0]["statistics"]["commentCount"] == "0"):
        commentCount = 0
        comments = "comments disabled"
        
    else:
        commentCount = videoDetails["items"][0]["statistics"]["commentCount"]
        request = YOUTUBE.commentThreads().list(
            part='snippet',
            videoId=videoId,
            textFormat='plainText',
            maxResults=100
        )
        comments = request.execute()
    
    return comments


