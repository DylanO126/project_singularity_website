import os
from dotenv import load_dotenv, find_dotenv

#Debuging to make sure path is correct
#print(find_dotenv())

#Load API key from .env
load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
DB_URL = os.getenv("DB_URL", "sqlite:///videos.db")


