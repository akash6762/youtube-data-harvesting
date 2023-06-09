from scripts import YOUTUBE


__all__ = ["getChannelIdByName", 
           "getPlaylistId", 
           "getVideoIds", 
           "getVideoDetails",
           "makeVideoDetailsAndComments"]


def getChannelIdByName(channelName: str) -> str:
    request = YOUTUBE.search().list(
        q = channelName,
        type = "channel",
        part = "id",
        maxResults = 1
    )
    response = request.execute()
    channelId = response["items"][0]["id"]["channelId"]

    return channelId
    

def getPlaylistId(channelId: str) -> str:
    request = YOUTUBE.channels().list(
        part='contentDetails',
        id=channelId
    )
    response = request.execute()
    #jsonResponse = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    items = response.get("items", [])
    playlistId = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]
    
    return playlistId


def getVideoIds(playlistId: str) -> list[str]:
    videoDetails = []
    nextPageToken = None

    while True:
        request = YOUTUBE.playlistItems().list(
            playlistId=playlistId,
            part="snippet",
            maxResults=50,
            pageToken=nextPageToken
        )
        response = request.execute()
        videoDetails += response["items"]

        nextPageToken = response.get('nextPageToken')
        if nextPageToken is None:
            break

    videoIds = []
    for video in videoDetails:
        _id = video["snippet"]["resourceId"]["videoId"]
        videoIds.append(_id)

    return videoIds


def getVideoDetails(videoId):
    request = YOUTUBE.videos().list(
        id = videoId,
        part = "snippet, contentDetails, statistics"
    )
    response = request.execute()

    return response


def makeVideoDetailsAndComments(nameOrId: str, streamlitOption: str):

    channel_id = None
    if streamlitOption == "channel name":
        channel_id = getChannelIdByName(nameOrId)  # channel id
        
    if streamlitOption == "channel id":
        channel_id = nameOrId

        """
        If the second argument(streamlitOption) is 'channel name' it first scrapes the 
        channel id, if the argument(streamlitOption) is 'channel id' then push it forward
        """

    playlist_id = getPlaylistId(channel_id)  # playlist id
    video_ids = getVideoIds(playlist_id)  # list of all video ids

    # channel details
    request = YOUTUBE.channels().list(
        id=channel_id,
        part="snippet, statistics"
    )
    response = request.execute()
    channel_name = {
        "channel_name": response["items"][0]["snippet"]["title"],
        "channel_id": response["items"][0]["id"],
        "subscription_count": response["items"][0]["statistics"]["subscriberCount"],
        "channel_views": response["items"][0]["statistics"]["viewCount"],
        "channel_description": response["items"][0]["snippet"]["description"],
        "playlist_id": playlist_id
    }


    videoAndCommentsData = []
    for index, video_id in enumerate(video_ids):
        videoInfo = getVideoDetails(video_id)
        
        commentList = [] # the dictionary of comments gets appended here
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

    processedData = {
        "channel_name": channel_name,
        "video_and_comments_data": videoAndCommentsData
    }

    return processedData


if __name__ == '__main__':
    pass
    