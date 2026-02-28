import requests
import json
import time
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()
API_KEY = os.getenv("LASTFM_API_KEY")

def fetchTag(artist, track):
    time.sleep(0.5)
    try:
        res = requests.get("http://ws.audioscrobbler.com/2.0/", params={
            "method": "track.getTopTags",
            "artist": artist,
            "track": track,
            "api_key": API_KEY,
            "format": "json",
            "autocorrect": 1
        }, timeout=5)
        data = res.json()
        if "toptags" not in data or "tag" not in data["toptags"]:
            return artist, track, []
        tags = [tag["name"].lower().strip() for tag in data["toptags"]["tag"]][:5]
        return artist, track, tags
    except Exception:
        return artist, track, []

def run():
    with open("dataCollector/uniqueScrobbles.json", "r") as f:
        uniqueTracks = json.load(f)

    tagDB = {}
    try:
        with open("dataCollector/tagDB.json") as f:
            tagDB = json.load(f)
        print(f"Resuming from {len(tagDB)}")
    except FileNotFoundError:
        print("Starting anew")

    remaining = [
        (t["artist"], t["track"])
        for t in uniqueTracks
        if f"{t['artist']}|||{t['track']}" not in tagDB
    ]
    total = len(remaining)
    print(f"Tracks left: {total}")

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(fetchTag, a, t): (a, t) for a, t in remaining}
        completed = 0

        for future in as_completed(futures):
            artist, track, tags = future.result()
            key = f"{artist}|||{track}"
            tagDB[key] = tags
            completed += 1

            if completed % 100 == 0:
                with open("dataCollector/tagDB.json", "w") as f:
                    json.dump(tagDB, f)
                tagged = sum(1 for v in tagDB.values() if v)
                print(f"{completed}/{total} — {tagged} tagged so far")

    with open("dataCollector/tagDB.json", "w") as f:
        json.dump(tagDB, f, indent=2)

    tagged = sum(1 for v in tagDB.values() if v)
    print(f"\nDone. {tagged}/{total} tracks have tags.")

if __name__ == "__main__":
    run()
