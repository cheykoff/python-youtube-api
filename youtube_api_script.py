from googleapiclient.discovery import build
import os

youtube_api_key = os.environ.get('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=youtube_api_key)

request = youtube.channels().list(
    part='statistics',
    forUsername='schafer5'
)

response = request.execute()

print(response)
