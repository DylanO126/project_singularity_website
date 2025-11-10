from app.database import SessionLocal, add_channel
from youtube_api import get_channel_id
# List of channels to track (channel_id, name)
channels_to_add = ["@NeuroticGoose","@Hecuba39","@Ham-Corp","@DuckedGTNH", "@IX_Streams","@soycake", "@3ricbae",
                   "@Flurben", "@Dragonium10190", "@ChiefLogan_", "@glistew", "@jetlaggmc", "@Jolliwog", "@Mastiox"]

if __name__ == "__main__":
    session = SessionLocal()
    channel_ids_to_add = {}
    for username in channels_to_add:
        channel_ids_to_add[username] = get_channel_id(username)
    for name, channel_id in channel_ids_to_add.items():
        add_channel(session, channel_id, name)
    session.close()