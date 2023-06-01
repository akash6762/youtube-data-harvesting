from googleapiclient.discovery import build
import json
from config import YOUTUBE


def getVideoDetails(videoId):
    """

    Parameters
    ----------
    videoId: A list of video ids generated from getVideoIds function

    Returns: video details in json format
    -------

    """

    request = YOUTUBE.videos().list(
        id = videoId,
        part = "snippet, contentDetails, statistics"
    )
    response = request.execute()

    return response
