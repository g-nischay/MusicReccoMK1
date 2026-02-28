import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def getWeather(city="Chennai"):
    apiKey = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&units=metric"

    response = requests.get(url)
    data = response.json()

    return{
        "temperature": data["main"]["temp"],
        "condition": data["weather"][0]["main"],
        "humidity": data["main"]["humidity"],
        "feels_like": data["main"]["feels_like"]
    }

def getTimeContext():
    now = datetime.now()
    hour = now.hour
    if 5<=hour<12:
        dayTime = "morning"
    elif 12<=hour<17:
        dayTime = "afternoon"
    elif 17<=hour<21:
        dayTime = "evening"
    else:
        dayTime = "night"
    
    return{
        "hour": hour,
        "dayTime": dayTime,
        "weekDay": now.strftime("%A"),
        "isWeekend": now.weekday()>=5
    }

def buildContext(city="Chennai"):
    weather = getWeather(city)
    time = getTimeContext()

    return {**weather, **time}

if __name__ == "__main__":
    ctx = buildContext()
    for key, value in ctx.items():
        print(f"{key}: {value}")
