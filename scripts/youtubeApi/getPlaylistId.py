from googleapiclient.discovery import build
from config import YOUTUBE


def getPlaylistId(channelId: str) -> str:
    """

    Parameters
    ----------
    channelId: id of the YouTube channel, type = str

    Returns: playlist id of the given YouTube channel, type = str
    -------

    """

    request = YOUTUBE.channels().list(
        part = 'contentDetails',
        id = channelId
    )
    response = request.execute()
    playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    return playlist_id


