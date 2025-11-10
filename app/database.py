import logging
import os
from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from app.config import DB_URL

db_path = os.path.abspath('C:\\Users\\dylan\\Documents\\youtube_database_project\\videos.db')  # adjust as needed
print("Connecting to:", db_path)
engine = create_engine(f"sqlite:///{db_path}")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Channel(Base):
    __tablename__ = "channels"
    id = Column(String, primary_key=True) # channel_id
    name = Column(String)
    videos = relationship("Video", back_populates="channel")

class Video(Base):
    __tablename__ = "videos"
    id = Column(String, primary_key=True) # videp_id

    title = Column(String)
    published_at = Column(String)
    channel_id = Column(String, ForeignKey("channels.id"))

    channel = relationship("Channel", back_populates="videos")


def init_db():
    Base.metadata.create_all(bind=engine)

def add_channel(session, channel_id, name):
    try:
        existing = session.query(Channel).filter_by(id=channel_id).first()
        if not existing:
            session.add(Channel(id=channel_id, name=name))
            session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"Failed to add channel {name}: {e}")


def add_video(session, video_id, title, published_at, channel_id):
    try:
        existing = session.query(Video).filter_by(id=video_id).first()
        if not existing:
            new_video = Video(
                id=video_id,
                title=title,
                published_at=published_at,
                channel_id=channel_id
            )
            session.add(new_video)
            session.commit()
            logging.INFO(f"Saved video: {title}")
    except Exception as e:
        logging.error(f"Failed to add video {title}: {e}")