import unittest
from app.youtube_api import get_latest_uploads, get_channel_id
from app.database import SessionLocal, Channel

class TestYouTubeAPI(unittest.TestCase):
    def test_valid_channel(self):
        videos = get_latest_uploads("UC_x5XG1OV2P6uZZ5FSM9Ttw")
        self.assertIsInstance(videos, list)

    def test_invalid_channel(self):
        videos = get_latest_uploads("invalid_id")
        self.assertEqual(videos, [])


def test_latest_uploads():
    # Replace with a real channel ID (e.g., Google Developers)
    channel_id = "UCJzyqivEVGq4NVOdpd8HLGg"
    videos = get_latest_uploads(channel_id, max_results=3)

    assert isinstance(videos, list), "Expected a list of videos"
    assert len(videos) > 0, "No videos returned"
    for video in videos:
        print(f"{video['publishedAt']} - {video['title']} (https://youtu.be/{video['videoId']})")

def list_channels():
    session = SessionLocal()
    channels = session.query(Channel).all()
    if channels:
        print("Tracked channels:")
        for ch in channels:
            print(f"- {ch.name} ({ch.id})")
    else:
        print("No channels found.")
    session.close()


if __name__ == "__main__":
   get_channel_id("@Hecuba39")
   test_latest_uploads()
   list_channels()

