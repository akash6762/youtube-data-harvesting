from googleapiclient.discovery import build
from config import YOUTUBE


def getVideoIds(PlaylistId: str) -> list:
    """

    Parameters
    ----------
    PlaylistId: playlist id of a YouTube channel

    Returns: list of video ids of the given YouTube channel
    -------

    """
    videoDetails = []
    nextpageToken = None

    while True:
        request = YOUTUBE.playlistItems().list(
            playlistId=PlaylistId,
            part="snippet",
            maxResults=50,
            pageToken=nextpageToken
        )
        response = request.execute()
        videoDetails += response["items"]

        nextpageToken = response.get('nextPageToken')
        if nextpageToken is None:
            break

    videoIds = []
    for video in videoDetails:
        _id = video["snippet"]["resourceId"]["videoId"]
        videoIds.append(_id)

    return videoIds
