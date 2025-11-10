from app.youtube_api import get_latest_uploads
from app.database import init_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import SessionLocal, Video

app = FastAPI()



if __name__ == "__main__":
    init_db()
    print("Database initialized.")
