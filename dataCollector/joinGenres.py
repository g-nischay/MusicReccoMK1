import json
from collections import Counter

def loadAllDatabases():
    with open("dataCollector/scrobblesRaw.json", "r") as f:
        scrobbles = json.load(f)
    with open("dataCollector/tagDB.json", "r") as f:
        tagDB = json.load(f)
    with open("dataCollector/artistGenre.json", "r") as f:
        artistGenre = json.load(f)
    with open("dataCollector/artistTagDB.json", "r") as f:
        artistTag = json.load(f)
    return scrobbles,tagDB,artistGenre,artistTag

def getTagsForScrobble(scrobble, tagDB, artistGenres, artistTags):

    trackKey = scrobble["artist"]+"|||"+scrobble["track"]

    spotify = artistGenres.get(scrobble["artist"], [])
    aTags = artistTags.get(scrobble["artist"], [])
    tTags = tagDB.get(trackKey, [])

    if spotify:
        final, source = spotify, "spotify"
    elif aTags:
        final, source = aTags, "lastfmArtist"
    else:
        final, source = [], "none"
    
    if tTags:
        final, source = tTags, "lastfmTrack"

    return final,source

def run():
    scrobbles, tagDB, artistGenres, artistTags = loadAllDatabases()

    enriched = []
    stats = Counter()

    for scrobble in scrobbles:
        tags, source = getTagsForScrobble(scrobble, tagDB, artistGenres, artistTags)

        if tags:
            scrobble["tags"] = tags
            scrobble["tagSource"] = source
            enriched.append(scrobble)
            stats[source]+=1
        else:
            stats["none"] +=1

    with open("dataCollector/scrobbleEnriched.json", "w") as f:
        json.dump(enriched, f, indent=2)
    
    print(f"Total: {len(scrobbles)}")
    print(f"Spotify: {stats["spotify"]}")
    print(f"lastfm Artist: {stats["lastfmArtist"]}")
    print(f"lastfm Track: {stats["lastfmTrack"]}")
    print(f"dropped: {stats["none"]}")

if __name__ == "__main__":
    run()
