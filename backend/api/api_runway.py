# backend/api_runway.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")

def generate_video(prompt, image_url=None):
    url = "https://api.runwayml.com/v1/generate"

    headers = {
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt
    }

    if image_url:
        payload["image_url"] = image_url

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Runway API error: {response.text}")
