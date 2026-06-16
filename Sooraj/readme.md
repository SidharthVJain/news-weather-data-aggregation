# Personalized Daily Briefing 📰🌤️

A simple, beginner-friendly Python application that creates a custom daily briefing. It aggregates current weather data, top news headlines, and a random joke by connecting to multiple APIs, and then saves your briefing history to a local JSON file. 

## Features
* **Live Weather Data:** Fetches the current temperature and conditions for any city.
* **Curated News:** Pulls the top 5 latest headlines based on your chosen topic.
* **Daily Joke:** Retrieves a random joke to start your day off right.
* **Data Logging:** Automatically saves your generated briefings into a `saved_briefing.json` file.
* **Simple GUI:** Uses Tkinter to display the results in a clean, easy-to-read desktop window.

## Prerequisites
Before running this project, make sure you have the following installed:
* Python 3.x
* `requests` and `python-dotenv` libraries
* **Linux Users:** If you are on Fedora or a similar Linux distribution, ensure Tkinter is installed on your system (`sudo dnf install python3-tkinter`).
