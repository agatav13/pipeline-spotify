import requests
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
URL: str = "https://accounts.spotify.com/api/token"
