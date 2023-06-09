from googleapiclient.discovery import build

__all__ = ["YOUTUBE"]

API_KEY: str = "AIzaSyAgwzSCHzY0_nLZPzOzQ3jSoWatEI6Njsk" # api key
YOUTUBE: object = build("youtube", "v3", developerKey=API_KEY)
