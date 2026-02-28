import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id = os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
))

def fetchArtistGenres(artist):
    try:
        res = sp.search(q=f"artist:{artist}", type="artist", limit=1)
        items = res["artists"]["items"]

        if not items:
            return []
        
        return items[0]["genres"][:5]
    
    except Exception :
        return []

def run():
    with open("dataCollector/uniqueScrobbles.json", "r") as file:
        uniqueTracks = json.load(file)
    
    genreDB = {}
    total = len(uniqueTracks)

    try:
        with open("dataCollector/artistGenre.json" ) as file:
            genreDB = json.load(file)
            print(f"Resuming from {len(genreDB)} artists")
    except FileNotFoundError:
        print("Starting anew")

    for i, track in enumerate(uniqueTracks):
        artist = track["artist"]

        if artist in genreDB:
            continue

        genres = fetchArtistGenres(artist)
        genreDB[artist] = genres
        if i%100 ==0:
            with open("dataCollector/artistGenre.json", "w") as file:
                json.dump(genreDB, file)
            tagged = sum(1 for v in genreDB.values() if v)
            print(f"{i}/{total} - {tagged} artists with genres so far")

        time.sleep(0.1)

    with open("dataCollector/artistGenre.json", "w") as file:
        json.dump(genreDB, file, indent=2)
    
    tagged = sum(1 for v in genreDB.values() if v)
    print("\n done.")

if __name__ == "__main__":
    run()
