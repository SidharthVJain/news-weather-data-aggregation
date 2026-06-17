import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


def get_news(topic):
    """
    Fetch top 5 news articles related to the given topic.
    """

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={topic}&"
        f"sortBy=publishedAt&"
        f"pageSize=5&"
        f"language=en&"
        f"apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        return data.get("articles", [])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []


def get_weather(city):
    """
    Fetch current weather data for the given city.
    """

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&"
        f"appid={WEATHER_API_KEY}&"
        f"units=metric"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather: {e}")
        return None


def display_briefing(topic, city):
    """
    Display personalized daily briefing.
    """

    news_articles = get_news(topic)
    weather_data = get_weather(city)

    print("\n" + "=" * 50)
    print("        PERSONALIZED DAILY BRIEFING")
    print("=" * 50)

    print(f"\nTopic: {topic}")
    print(f"City: {city}")

    print("\nWEATHER REPORT")
    print("-" * 30)

    if weather_data:

        condition = weather_data["weather"][0]["description"].title()
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]

        print(f"Condition   : {condition}")
        print(f"Temperature : {temperature}°C")
        print(f"Humidity    : {humidity}%")

    else:
        print("Weather data unavailable.")

    print("\nTOP 5 NEWS HEADLINES")
    print("-" * 30)

    if news_articles:

        for i, article in enumerate(news_articles, start=1):

            title = article.get("title", "No Title")
            source = article.get("source", {}).get("name", "Unknown Source")

            print(f"\n{i}. {title}")
            print(f"   Source: {source}")

    else:
        print("No news articles found.")

    print("\n" + "=" * 50)


def main():

    print("Welcome to the Daily Briefing App")

    topic = input("Enter a topic (AI, Technology, Sports, Finance, etc.): ")
    city = input("Enter a city name: ")

    display_briefing(topic, city)


if __name__ == "__main__":
    main()