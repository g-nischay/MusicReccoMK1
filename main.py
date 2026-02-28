from contextCollector import buildContext
from spotifyConnector import searchSongsByMood
from llmRecommender import getReccomendations

def run():
    print("Real-Time music recco Service\n(1/3)\n")
    
    ctx = buildContext()
    for key, value in ctx.items():
        print(f"{key}: {value}")
    
    print("\n(2/3)\n")
    moodQuery = getReccomendations(ctx)

    print("\n(3/3)\n")
    songs = searchSongsByMood(moodQuery, limit=5)

    print("Songs for right now:")
    for i, song in enumerate(songs, 1):
        print(f"\n {i}. {song['name']}- {song['artist']}")
        print(f"Popularity: {song['popularity']}/100")
        print(f"Listen: {song['spotify_url']}")

if __name__ == "__main__":
    run()
