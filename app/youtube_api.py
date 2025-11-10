import logging
from googleapiclient.discovery import build
from app.config import YOUTUBE_API_KEY
import json
#Initialize YouTube API client

def safe_api_call(callable, *args, **kwargs):
    try:
        return callable(*args, **kwargs).execute()
    except Exception as e:
        logging.error(f"API call failed: {e}")
        return {}

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def get_latest_uploads(channel_id, max_results=5):
    # Step 1: Get the Uploads playlist ID
    channel_response = safe_api_call(youtube.channels().list,
                                     part="contentDetails",
                                     id=channel_id
                                     )

    #print(json.dumps(channel_response, indent=2))
    uploads_playlist_id =  channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # Step 2: Get videos from the uploads playlist
    playlist_response = safe_api_call(youtube.playlistItems().list,
                                      part="snippet",
                                      playlistId=uploads_playlist_id,
                                      maxResults=max_results
                                      )
    #print(json.dumps(playlist_response, indent=2))
    videos = []
    for item in playlist_response["items"]:
        video = {"title": item["snippet"]["title"],
                 "videoId": item["snippet"]["resourceId"]["videoId"],
                 "publishedAt": item["snippet"]["publishedAt"]
                 }
        videos.append(video)
    return videos
def get_channel_id(channel_username):
    response = safe_api_call(youtube.search().list,
                             part="snippet",
                             q=channel_username,
                             type="channel",
                             maxResults=1
                             )
    if response["items"]:
        channel_id = response["items"][0]["snippet"]["channelId"]
        title = response["items"][0]["snippet"]["title"]
        print(f"Channel: {title}\nChannel ID: {channel_id}")
        return channel_id
    else:
        print("No channel found.")
        return None
