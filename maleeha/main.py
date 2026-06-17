import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

NEWS_API_KEY    = os.getenv("NEWS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def fetch_news(topic):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q":        topic,
        "apiKey":   NEWS_API_KEY,
        "pageSize": 5,
        "sortBy":   "publishedAt",
        "language": "en",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code == 401:
            print(" News API Error: Invalid API key.")
            return None
        if response.status_code != 200:
            print(f" News API Error: {data.get('message', 'Unknown error')}")
            return None
        if data["totalResults"] == 0:
            print(f"  No news found for topic: '{topic}'")
            return None

        articles = []
        for article in data["articles"]:
            articles.append({
                "title":  article.get("title", "No title"),
                "source": article.get("source", {}).get("name", "Unknown"),
                "url":    article.get("url", ""),
            })
        return articles

    except requests.exceptions.ConnectionError:
        print(" News API Error: Could not connect to News API.")
        return None
    except requests.exceptions.Timeout:
        print("News API request timed out.")
        return None


def fetch_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q":     city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if response.status_code == 401:
            print(" Weather API Error: Invalid API key.")
            return None
        if response.status_code == 404:
            print(f"City not found: '{city}'. Check the spelling and try again.")
            return None
        if response.status_code != 200:
            print(f"Weather API Error: {data.get('message', 'Unknown error')}")
            return None

        return {
            "city":        data["name"],
            "country":     data["sys"]["country"],
            "condition":   data["weather"][0]["description"].title(),
            "temperature": data["main"]["temp"],
            "feels_like":  data["main"]["feels_like"],
            "humidity":    data["main"]["humidity"],
        }

    except requests.exceptions.ConnectionError:
        print(" Network error: Could not connect to Weather API.")
        return None
    except requests.exceptions.Timeout:
        print(" Weather API request timed out.")
        return None


def display_briefing(topic, news, weather):
    now = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p")

    print("\n" + "=" * 55)
    print(f"  YOUR PERSONALIZED DAILY BRIEF")
    print(f"  {now}")
    print("=" * 55)

    if weather:
        print(f"\n WEATHER — {weather['city']}, {weather['country']}")
        print(f"   Condition   : {weather['condition']}")
        print(f"   Temperature : {weather['temperature']}C (Feels like {weather['feels_like']}C)")
        print(f"   Humidity    : {weather['humidity']}%")
    else:
        print("\n WEATHER — Unavailable")

    print(f"\n TOP NEWS — {topic.upper()}")
    if news:
        for i, article in enumerate(news, start=1):
            print(f"\n   {i}. {article['title']}")
            print(f"      Source : {article['source']}")
            print(f"      URL    : {article['url']}")
    else:
        print("   No news articles available.")

    print("\n" + "=" * 55)

def save_briefing(topic, news, weather):
    briefing = {
        "generated_at": datetime.now().isoformat(),
        "topic":        topic,
        "weather":      weather,
        "news":         news,
    }
    with open("briefing.json", "w") as f:
        json.dump(briefing, f, indent=4)
    print("\n Briefing saved to briefing.json")


def validate_keys():
    if not NEWS_API_KEY:
        print(" NEWS_API_KEY is missing from your .env file.")
        return False
    if not WEATHER_API_KEY:
        print(" WEATHER_API_KEY is missing from your .env file.")
        return False
    return True
def main():
    print("Welcome to your Daily Brief Generator!")

    if not validate_keys():
        return

    topic = input("\nEnter a topic of interest (e.g. AI, Sports, Finance): ").strip()
    city  = input("Enter your city name: ").strip()

    if not topic or not city:
        print("Topic and city cannot be empty.")
        return

    print("\nFetching your personalized briefing...\n")

    news    = fetch_news(topic)
    weather = fetch_weather(city)

    display_briefing(topic, news, weather)
    save_briefing(topic, news, weather)


if __name__ == "__main__":
    main()