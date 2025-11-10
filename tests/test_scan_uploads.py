from unittest.mock import patch
from app.scan_uploads import scan_channels_for_keyword

@patch("app.youtube_api.get_latest_uploads")
def test_keyword_match(mock_get):
    mock_get.return_value = [
        {"videoId": "123", "title": "Singularity Explained", "publishedAt": "2025-11-05T12:00:00Z"}
    ]
    scan_channels_for_keyword("singularity")
