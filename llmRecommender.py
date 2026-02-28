from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def getMoodQuery(context):
    prompt = f"""
    You are a music recommendation AI with deep knowledge of how environment 
    and mood relate to music choices.
    
    Given this real-time context:
    - Weather: {context['condition']}, {context['temperature']}°C, humidity {context['humidity']}%
    - Time of day: {context['dayTime']} ({context['hour']}:00)
    - Day: {context['weekDay']} ({'Weekend' if context['isWeekend'] else 'Weekday'})
    
    Return ONLY a short Spotify search query (5-8 words) that would find 
    music perfectly fitting this context. No explanation, just the query.
    
    Example outputs:
    - "late night lo-fi chill study beats"
    - "sunny morning upbeat indie pop"
    - "rainy evening melancholic acoustic"
    """

    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages=[{
            "role":"user",
            "content": prompt
        }],
        temperature = 0.7,
        max_tokens = 50,
    )

    moodQuery = response.choices[0].message.content.strip()
    return moodQuery

def getReccomendations(ctx):
    moodQuery = getMoodQuery(ctx)
    print(f"Moodquery: '{moodQuery}'")
    return moodQuery

if __name__ == "__main__":
    from contextCollector import buildContext
    ctx = buildContext()
    getReccomendations(ctx)
