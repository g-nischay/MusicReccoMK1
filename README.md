# MusicReccoMK1

---

## What's achieved till now?

Can provide basic reccomendation based solely on the weather and time of the day based off of the device timezone and city location set.

Will need personal api keys from **[OpenWeathermap](https://openweathermap.org)**, **[Groq](https://console.groq.com/dashboard/metrics)**, and **[Spotify](https://developer.spotify.com/)**.

Data collecting and cleaning pipeline in [DataCollector](https://github.com/g-nischay/MusicReccoMK1/tree/main/dataCollector) folder with seperately implemented functions for:

-Fetching listening history from [Last.fm](https://last.fm/)

-Seperate them into unique tracks

-Fetch genre tags for the tracks from [Last.fm](https://last.fm/) for which they're available

-Fetch [spotify](https://open.spotify.com/) genre categorization for all the unique artists

-Also fetch [Last.fm](https://last.fm/) genre categorization for all the
unique artists

-Join and layer the acquited data onto the raw data, first the track's primary artist checked in [spotify](https://open.spotify.com/) artist genre list, followed by [Last.fm](https://last.fm/) artist list, finally if direct data is available for the track on [Last.fm](https://last.fm/), its used instead for its richness.

## Whats to follow?

-Fetching data from fitness tracking app(currently [samsung fitness](https://www.samsung.com/us/apps/samsung-health/) and maybe [Mi Fitness](https://watch.iot.mi.com/download-apps-v3.html) planned)

-Fetch hour wise Weather data based on the user's geographical location at that timestamp

-Cleaning the data into a usable format and map it to correct time stamps

-Map it all to each other

-Train a XGBoost model with various parameters

-idk

---

## Bis Baldd
