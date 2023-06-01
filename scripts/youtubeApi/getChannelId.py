# importing dependencies
from scripts import YOUTUBE


def getChannelIdByName(channelName: str) -> str:
    """

    Parameters
    ----------
    channelName: name of the YouTube channel, type: str

    Returns: channel id of the YouTube channel, type: str
    -------

    """
    request = YOUTUBE.search().list(
        q = channelName,
        type = "channel",
        part = "id",
        maxResults = 1
    )
    response = request.execute()
    channel_id = response["items"][0]["id"]["channelId"]

    return channel_id
