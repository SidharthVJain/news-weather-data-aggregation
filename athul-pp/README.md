# Personalized Daily Brief

A Python command-line application that aggregates data from multiple APIs to provide a personalized daily briefing. It fetches current weather for a specific city and the top 5 recent news headlines for a chosen topic.

## Features

* Combines data from WeatherAPI and NewsAPI.
* Securely loads API credentials using environment variables (`.env`).
* Gracefully handles empty search results and invalid inputs.
* Displays article source names and direct URLs.

## Prerequisites

* Python 3.x
* Git
* API Keys from [NewsAPI](https://newsapi.org/) and [WeatherAPI](https://www.weatherapi.com/)

## Installation and Setup

1. Clone the repository and navigate to the project directory:
```bash
cd Athul-PP

```


2. Create and activate a virtual environment.
3. Install the required dependencies:
```bash
pip install -r requirements.txt

```


4. Create a `.env` file in the root directory and add your API keys:
```env
NEWS_API_KEY=your_news_api_key_here
WEATHER_API_KEY=your_weather_api_key_here

```



## Usage

Run the script using Python:

```bash
python main.py

```

When prompted, enter a topic of interest and your current city.

## Author

Athul P P