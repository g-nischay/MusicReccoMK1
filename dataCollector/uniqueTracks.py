import json
from collections import Counter
inFile = "dataCollector/scrobblesRaw.json"
outFile = "dataCollector/uniqueScrobbles.json"

with open(inFile, "r") as f:
    scrob = json.load(f)

trackCounts = Counter(
    (s["artist"], s["track"]) for s in scrob
)

uniqueTracks = [
    {"artist": artist,
    "track": track, "play_count": count}
    for (artist, track), count in trackCounts.most_common()
]

with open(outFile, "w+") as file:
    json.dump(uniqueTracks, file, indent=2)

print(f"total Scrobbles: {len(scrob)}")
print(f"unique Scrobbles: {len(uniqueTracks)}")
