import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import time
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id = os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
))

def fetchArtistGenres(artist):
    try:
        res = sp.search(q=artist, type="artist", limit=3)
        items = res["artists"]["items"]

        if not items:
            return artist, []
        
        for item in items:
            if item["name"].lower() == artist.lower():
                return artist, item["genres"][:5]
            
        return artist, items[0]["genres"][:5]
    
    except Exception :
        return artist, []

def run():
    with open("dataCollector/uniqueScrobbles.json", "r") as file:
        uniqueTracks = json.load(file)
    
    uniqueArtists = list(set(t["artist"] for t in uniqueTracks))
    genreDB = {}

    try:
        with open("dataCollector/artistGenre.json" ) as file:
            genreDB = json.load(file)
            print(f"Resuming from {len(genreDB)} artists")
    except FileNotFoundError:
        print("Starting anew")

    remaining = [a for a in uniqueArtists if a not in genreDB]
    
    total = len(remaining)
    
    print(f"{total} artists left to fetch")
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(fetchArtistGenres, a): a for a in remaining}
        completed = 0

        for future in as_completed(futures):
            artist, genres = future.result()
            genreDB[artist] = genres
            completed +=1
            time.sleep(0.3)

            if completed % 100 == 0:
                with open("dataCollector/artistGenre.json", "w") as f:
                    json.dump(genreDB, f)
                tagged = sum(1 for v in genreDB.values() if v)
                print(f"{completed}/{total} we've {tagged} artists so far")

    with open("dataCollector/artistGenre.json", "w") as file:
        json.dump(genreDB, file, indent=2)
    
    tagged = sum(1 for v in genreDB.values() if v)
    print("\n done.")

if __name__ == "__main__":
    run()
