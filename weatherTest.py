import requests
import os
from dotenv import load_dotenv

load_dotenv()

def getWeather(city="Chennai"):
    apiKey = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&units=metric"

    response = requests.get(url)
    data = response.json()

    # print("Raw API response:", data)
    return{
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["main"],
        "humidity": data["main"]["humidity"],
        "feels_like": data["main"]["feels_like"]
    }

# weather = getWeather()
print(getWeather())
