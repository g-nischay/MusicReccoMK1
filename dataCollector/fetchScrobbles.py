import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LASTFM_API_KEY")

USERNAME = os.getenv("LASTFM_USERNAME")
outFile = "dataCollector/scrobblesRaw.json"

def fetchAllScrobbles():
    allTracks = []
    page=1
    totalPages=1
    
    while page<=totalPages:
        print(f"fetching page {page}/{totalPages}\n")

        res = requests.get("https://ws.audioscrobbler.com/2.0/", params={
            "method":"user.getRecentTracks",
            "user": USERNAME,
            "api_key": API_KEY,
            "format": "json",
            "limit": 200,
            "page": page,
        })
        data = res.json()

        totalPages = int(data["recenttracks"]["@attr"]["totalPages"])
        tracks = data["recenttracks"]["track"]

        for track in tracks:
            if isinstance(track, dict) and "@attr" in track:
                if track["@attr"].get("nhowplaying"):
                    continue

            if "date" not in track:
                continue

            allTracks.append({
                "timestamp": int(track["date"]["uts"]),
                "track": track["name"],
                "artist": track["artist"]["#text"],
                "album": track["album"]["#text"]
            })
        page+=1
        print(f"Current recent track: {allTracks[-1]["track"]}\n")
        time.sleep(0.25)
    return allTracks

if __name__=="__main__":
    print(f"Startinbg the fetch for {USERNAME}:\n")
    scrobbles = fetchAllScrobbles()
    with open(outFile, "w+") as file:
        json.dump(scrobbles, file)
    print(f"successfully fetched {len(scrobbles)} scrobbles.\n")
