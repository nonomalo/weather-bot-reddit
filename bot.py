import praw
import config
import requests
import json

def main():
    reddit = praw.Reddit(username = config.username,
                        password = config.password,
                        client_id = config.client_id,
                        weather_api = config.weather_api,
                        user_agent = "current-weather-bot v0.0.1")

    reddit.validate_on_submit=True

    subreddit = reddit.subreddit("all")

    # have bot respond to comments with its name
    for comment in subreddit.stream.comments():
        if comment.body.startswith("!current-weather-bot"):
            city = comment.body.split()[1]
            full_url = get_api_url(city)
            weather = get_weather(full_url)
            formatted_weather = format_weather(weather)
            comment.reply(formatted_weather)

def get_api_url(city):
    weather_url = "http://api.openweathermap.org/data/2.5/weather?"
    return weather_url + f"q={city}&appid={config.weather_api}"

def get_weather(full_url):
    # request weather info for desired city and give response
    weather_request = requests.get(full_url)
    weather_data = weather_request.json()

    city = f"**City:** {weather_data['name']}, {weather_data['sys']['country']}"
    temperature = f"**Temperature:** {get_temperature(weather_data)}\N{DEGREE SIGN}F"
    conditions = f"**Conditions:** {weather_data['weather'][0]['description']}"
    humidity = f"**Humidity:** {weather_data['main']['humidity']}%"

    weather = [city, temperature, conditions, humidity]
    return weather

def get_temperature(weather):
    """Convert temperature from Kelvin to Fahrenheit"""
    kelvin = weather['main']['temp']
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return round(fahrenheit, 1)

def format_weather(weather):
    """Concatenate list of string and add a space inbetween"""
    formatted_weather = ""
    for element in weather:
        formatted_weather += " " + element
    return formatted_weather

if __name__ == "__main__":
    main()
