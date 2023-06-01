from googleapiclient.discovery import build

API_KEY = "AIzaSyAgwzSCHzY0_nLZPzOzQ3jSoWatEI6Njsk" # api key
YOUTUBE = build("youtube", "v3", developerKey=API_KEY)