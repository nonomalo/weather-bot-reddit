import praw
import config
import requests
import json

def get_api_url(city):
    weather_url = "http://api.openweathermap.org/data/2.5/weather?"
    return weather_url + f"q={city}&appid={config.weather_api}"

def get_weather(full_url):
    # request weather info for desired city and give response
    weather_request = requests.get(full_url)
    weather_data = weather_request.json()

    city = f"City: {weather_data['name']}"

    temperature_kelvin = weather_data['main']['temp']
    temperature_fahrenheit = round(temperature_kelvin - 273, 1)
    temperature = f"Temperature: {temperature_fahrenheit}\N{DEGREE SIGN}F"

    conditions = f"Conditions: {weather_data['weather'][0]['description']}"

    humidity = f"Humidity: {weather_data['main']['humidity']}%"
    weather = [city, temperature, conditions, humidity]
    return weather


reddit = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    weather_api = config.weather_api,
                    user_agent = "current-weather-bot v0.0.1")

reddit.validate_on_submit=True

subreddit = reddit.subreddit("test")

# make a post on "test" subreddit
subreddit.submit("Test Submission", url="https://reddit.com")

# have bot respond to comments with its name
for comment in subreddit.stream.comments():
    if comment.body.startswith("!current-weather-bot"):
        city = comment.body.split()[1]
        full_url = get_api_url(city)
        weather = get_weather(full_url)
        comment.reply(weather)
