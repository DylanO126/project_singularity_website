import logging
import os
from app.database import SessionLocal, Channel, add_video
from app.youtube_api import get_latest_uploads
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


# Setup logging

logging.basicConfig(
    filename="scan_uploads.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def channel_scan_for_keyword(keyword="singularity"):
    session = SessionLocal()
    try:
        channels = session.query(Channel).all()
        if not channels:
            logging.warning("No channels found in database")
            return

        for ch in channels:
            logging.info(f"Checking uploads for channel: {ch.name} ({ch.id})")
            try:
                videos = get_latest_uploads(ch.id)
                if not videos:
                    logging.info(f"No videos returned for {ch.name}")
                    continue
                for v in videos:
                    if keyword.lower() in v["title"].lower():
                        try:
                            add_video(session, v["videoId"], v["title"], v["publishedAt"], ch.id)
                            logging.info(f"Saved video: {v['title']}")
                            video_url = f"https://youtu.be/{v['videoId']}"
                            send_email_alert(v["title"], video_url, ch.name)
                        except Exception as e:
                            logging.error(f"Failed to save video {v['title']}: {e}")
            except Exception as e:
                logging.error(f"Error fetching uploads for {ch.name}: {e}")
    except Exception as e:
        logging.critical(f"Database error: {e}")
    finally:
        session.close()
        logging.info("Scan complete.")
        with open("last_updated.txt", "w") as f:
            f.write(datetime.now().isoformat())


def send_email_alert(video_title, video_url, channel_name):
    sender = os.getenv("EMAIL_SENDER")
    recipient = os.getenv("EMAIL_RECIPIENT")
    password = os.getenv("EMAIL_PASSWORD")
    subject = f"New Video Match: {video_title}"

    body = f"""A new video from {channel_name} matches your keyword:\n\n{video_title}\n{video_url}"""

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        logging.info(f"Email sent for video: {video_title}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

if __name__ == "__main__":
    channel_scan_for_keyword()

