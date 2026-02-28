import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
        )
    )

# def getSongFeature(trackName, artist=""):
#     res = sp.search(
#         q=f"{trackName} {artist}",
#         limit=1,
#         type="track"
#         )
#     if not res["tracks"]["items"]:
#         print(f"Song not found: {trackName}")
#         return None
#     track = res["tracks"]["items"][0]
#     trackId = track["id"]

#     features = sp.audio_features(trackId)[0]

#     return{
#         "name": track["name"],
#         "artist": track["artists"][0]["name"],
#         "energy": features["energy"],
#         "valence": features["valence"],
#         "tempo": features["tempo"],
#         "danceability": features["danceability"],
#         "acousticness": features["acousticness"],
#         "instrumentalness": features["instrumentalness"]
#     }

def searchSongsByMood(moodQuery, limit = 10):
    res = sp.search(q=moodQuery, limit=limit, type="track")
    songs = []

    for track in res["tracks"]["items"]:
        songs.append({
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "spotify_url": track["external_urls"]["spotify"],
            "popularity": track["popularity"],
            "preview_url": track["preview_url"]
        })
        
    return songs

if __name__ == "__main__":
    # song = getSongFeature("Blinding Lights", "The Weeknd")
    # for key, value in song.items():
    #     print(f"{key}: {value}")
    
    # print("\n")

    songs = searchSongsByMood("rainy day chill", limit=5)
    for i in songs:
        print(f"{i}")
