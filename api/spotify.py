import base64
import os

import requests
from dotenv import load_dotenv

load_dotenv()

client_id: str | None = os.getenv("CLIENT_ID")
client_secret: str | None = os.getenv("CLIENT_SECRET")

client_creds: str = f"{client_id}:{client_secret}"
client_creds_b64: bytes = base64.b64encode(client_creds.encode())

token_url: str = "https://accounts.spotify.com/api/token"

token_data: dict[str, str] = {"grant_type": "client_credentials"}

token_headers: dict[str, str] = {"Authorization": f"Basic {client_creds_b64.decode()}"}

req = requests.post(token_url, data=token_data, headers=token_headers, timeout=10)
print(req.status_code)

token_response_data = req.json()
print(token_response_data)
