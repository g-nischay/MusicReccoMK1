import requests
import json
import time
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()
API_KEY = os.getenv("LASTFM_API_KEY")

def fetchArtistTags(artist):
    time.sleep(0.5)
    try:
        res = requests.get("http://ws.audioscrobbler.com/2.0/", params={
            "method": "artist.getTopTags",
            "artist": artist,
            "api_key": API_KEY,
            "format": "json",
            "autocorrect": 1
        }, timeout=5)
        data = res.json()
        if "toptags" not in data or "tag" not in data["toptags"]:
            return artist, []
        tags = [tag["name"].lower().strip() for tag in data["toptags"]["tag"]][:5]
        return artist, tags
    except Exception:
        return artist, []

def run():
    with open("dataCollector/uniqueScrobbles.json") as f:
        uniqueTracks = json.load(f)

    uniqueArtists = list(set(t["artist"] for t in uniqueTracks))
    print(f"Unique artists: {len(uniqueArtists)}")

    artistTagDB = {}
    try:
        with open("dataCollector/artistTagDB.json") as f:
            artistTagDB = json.load(f)
        print(f"Resuming from {len(artistTagDB)}")
    except FileNotFoundError:
        print("Starting anew")

    remaining = [a for a in uniqueArtists if a not in artistTagDB]
    total = len(remaining)
    print(f"{total} artists left to fetch")

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(fetchArtistTags, a): a for a in remaining}
        completed = 0

        for future in as_completed(futures):
            artist, tags = future.result()
            artistTagDB[artist] = tags
            completed += 1

            if completed % 100 == 0:
                with open("dataCollector/artistTagDB.json", "w") as f:
                    json.dump(artistTagDB, f)
                tagged = sum(1 for v in artistTagDB.values() if v)
                print(f"{completed}/{total} — {tagged} tagged so far")

    with open("dataCollector/artistTagDB.json", "w") as f:
        json.dump(artistTagDB, f, indent=2)

    tagged = sum(1 for v in artistTagDB.values() if v)
    print(f"\nDone.")

if __name__ == "__main__":
    run()
