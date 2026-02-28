import requests
import json
import time
import os
from dotenv import load_env

load_env()

API_KEY = os.getenv("LASTFM_API_KEY")

def fetchTag(artist, track):
    try:
        res = requests.get("https://ws.audioscrobbler.com/2.0/",params={
            "method": "track.getTopTags",
            "artist": artist,
            "track": track,
            "api_key": API_KEY,
            "format": "json,"
            "autocorrect": 1
        }, timeout=5)

        data = res.json()
        
        if "toptags" not in data:
            return []
        if "tag" not in data["toptags"]
            return []
        tags = [
            tag["name"].lower().strip()
            for tag in data["toptags"]["tag"]
            if int(tag["count"])>10
        ]
        return tags
    except Exception as e:
        return []
