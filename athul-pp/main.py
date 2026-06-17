import os
import requests
from dotenv import load_dotenv

# 1. Load environment variables from the .env file
load_dotenv()

# Grab the keys and store them in variables
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_weather(city):
    """Fetches weather data for a given city."""
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        condition = data["current"]["condition"]["text"]
        temp = data["current"]["temp_c"]
        humidity = data["current"]["humidity"]
        return f"{condition}, {temp}°C, Humidity: {humidity}%"
    elif response.status_code == 400:
        return f"Could not find weather for '{city}'."
    elif response.status_code in [401, 403]:
        return "Weather API Key is invalid or missing!"
    else:
        return "Weather data currently unavailable."

def get_news(topic):
    """Fetches top 5 news articles for a given topic."""
    # pageSize=5 ensures we only get exactly 5 articles back to save bandwidth
    url = f"https://newsapi.org/v2/everything?q={topic}&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        
        if not articles:
            return [f"No recent news found for the topic: '{topic}'."]
            
        news_list = []
        for i, article in enumerate(articles, 1):
            title = article.get("title", "No Title")
            source = article.get("source", {}).get("name", "Unknown Source")
            url = article.get("url", "")
            news_list.append(f"{i}. {title} ({source})\n   Read more: {url}")
            
        return news_list
    elif response.status_code == 401:
        return ["News API Key is invalid or missing!"]
    else:
        return ["News data currently unavailable."]

def generate_briefing():
    # Make sure keys actually loaded before trying to run
    if not NEWS_API_KEY or not WEATHER_API_KEY:
        print("Error: API Keys are missing. Please check your .env file.")
        return

    print("=== Welcome to your Personalized Daily Brief ===")
    topic = input("Enter a topic of interest (e.g., AI, Sports, Space): ")
    city = input("Enter your current city (e.g., London, Tokyo): ")
    
    print("\nFetching your daily briefing...\n")
    
    # Fetch the data
    weather_info = get_weather(city)
    news_headlines = get_news(topic)
    
    # Display the results
    print("=" * 50)
    print(f"🌤️  WEATHER IN {city.upper()}")
    print("-" * 50)
    print(weather_info)
    print("\n" + "=" * 50)
    print(f"📰  TOP 5 NEWS HEADLINES: {topic.upper()}")
    print("-" * 50)
    
    for headline in news_headlines:
        print(headline)
        print() # Adds a blank line between articles
    print("=" * 50)

if __name__ == "__main__":
    generate_briefing()