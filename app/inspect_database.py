from app.database import SessionLocal, Channel, Video

def inspect_database():
    session = SessionLocal()

    # List all channels
    channels = session.query(Channel).all()
    print("\n📺 Channels:")
    if channels:
        for ch in channels:
            print(f"- {ch.name} ({ch.id})")
    else:
        print("No channels found.")

    # List all videos
    videos = session.query(Video).all()
    print("\n🎥 Videos:")
    if videos:
        for v in videos:
            print(f"- {v.title} ({v.id}) from {v.channel_id} at {v.published_at}")
    else:
        print("No videos found.")

    session.close()

if __name__ == "__main__":
    inspect_database()