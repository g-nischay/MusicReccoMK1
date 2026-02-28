import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LASTFM_API_KEY")

def fetchTag(artist, track):
    try:
        res = requests.get("https://ws.audioscrobbler.com/2.0/", params={
            "method": "track.getTopTags",
            "artist": artist,
            "track": track,
            "api_key": API_KEY,
            "format": "json",
            "autocorrect": 1
        }, timeout=5)

        data = res.json()

        if "toptags" not in data:
            return []
        if "tag" not in data["toptags"]:
            return []

        tags = [
            tag["name"].lower().strip()
            for tag in data["toptags"]["tag"]
        ][:5    ]
        return tags

    except Exception as e:
        return []

def run():
    with open("dataCollector/uniqueScrobbles.json", "r") as file:
        uniqueTracks = json.load(file)

    tagDB = {}
    total = len(uniqueTracks)

    try:
        with open("dataCollector/tagDB.json") as file:
            tagDB = json.load(file)
        print(f"Resuming from {len(tagDB)}")
    except FileNotFoundError:
        print("Starting anew")

    for i, track in enumerate(uniqueTracks):
        key = f"{track['artist']}|||{track['track']}"

        if key in tagDB:
            continue

        tags = fetchTag(track["artist"], track["track"])
        tagDB[key] = tags

        if i % 100 == 0:
            with open("dataCollector/tagDB.json", "w") as file:
                json.dump(tagDB, file)
            tagged = sum(1 for v in tagDB.values() if v)
            print(f"{i}/{total} — {tagged} tracks tagged so far")

        time.sleep(0.2)

    with open("dataCollector/tagDB.json", "w") as file:
        json.dump(tagDB, file, indent=2)

    tagged = sum(1 for v in tagDB.values() if v)
    print(f"\nDone. {tagged}/{total} tracks have tags.")

if __name__ == "__main__":
    run()
