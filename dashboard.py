import streamlit as st
from app.database import SessionLocal, Video, Channel
from sqlalchemy.orm import joinedload
from app.database import engine, Base
import os

Base.metadata.create_all(bind=engine)

st.title("Project Singularity Video List")


page_size = 10 #Number of videos per page
if "page" not in st.session_state:
    st.session_state.page = 1


session = SessionLocal()
videos = session.query(Video).options(joinedload(Video.channel)).order_by(Video.published_at.desc()).all()
channel = session.query(Channel).all()
session.close()

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("⬅️ Previous") and st.session_state.page > 1:
        st.session_state.page -= 1

with col2:
    if st.button("Next ➡️") and st.session_state.page < (len(videos) + page_size - 1) // page_size:
        st.session_state.page += 1

total_pages = (len(videos) + page_size - 1)
start = (st.session_state.page - 1) * page_size
end = start + page_size
page_videos = videos[start:end]

st.write(f"Showing videos {start + 1}–{min(end, len(videos))} of {len(videos)}")
if os.path.exists("last_updated.txt"):
    with open("last_updated.txt", "r") as f:
        last_updated = f.read()
    st.caption(f"🕒 Last updated: {last_updated.replace('T', ' ')[:16]}")

for v in page_videos:
    date_string = v.published_at.replace("T", " ")[:16]
    channel_url = f"https://www.youtube.com/channel/{v.channel_id}"
    thumbnail_url = f"https://img.youtube.com/vi/{v.id}/hqdefault.jpg"
    st.image(thumbnail_url, width=320)
    st.markdown(f"""
    ### [{v.title}](https://youtu.be/{v.id})
    - Published: {date_string}
    - Channel: {v.channel.name}
    - Channel Link: {channel_url}
    ---
    """)

