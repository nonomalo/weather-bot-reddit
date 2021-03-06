import praw
import config
import requests
import json

def main():
    """Respond to comments with the bot's name (!current-weather-bot) and a city on r/all with the
    name of the city, temperature (fahrenheit), conditions, and humidity."""
    reddit = get_credentials()
    reddit.validate_on_submit=True

    # have bot work on every subreddit
    subreddit = reddit.subreddit("all")

    # have bot respond to comments with its name
    for comment in subreddit.stream.comments():
        if comment.body.startswith("!current-weather-bot"):
            location = get_location(comment)
            full_url = get_api_url(location)
            weather = get_weather(full_url)
            comment.reply(weather)

def get_credentials():
    """Get credentials for bot account"""
    reddit = praw.Reddit(username = config.username,
                        password = config.password,
                        client_id = config.client_id,
                        client_secret = config.client_secret,
                        weather_api = config.weather_api,
                        user_agent = "current-weather-bot v0.0.1")
    return reddit

def get_location(comment):
    """Get full city name (and country if applicable) from comment"""
    # remove bot call from string
    location = comment.split.body('!current-weather-bot ', 1)[1]

    # if country code is included
    if ',' in location:
        country = get_country_code(location)
        city = location.split(', ')[0]
        return f"{city},{country}"
    
    # if comment just mentions city
    else:
        return location

def get_country_code(comment):
    country = comment.split(', ', 1)[1]
    return country

def get_api_url(city):
    """Get full url for api call"""
    weather_url = "http://api.openweathermap.org/data/2.5/weather?"
    return weather_url + f"q={city}&appid={config.weather_api}"

def get_weather(full_url):
    """Call on OpenWeatherMap to retrieve city, temperature, conditions, and humidity"""
    # request weather info for desired city and save response
    weather_request = requests.get(full_url)
    weather_data = weather_request.json()

    if check_for_error(weather_data) is False:
        # collect all desired weather conditions using the response
        city = f"**City:** {weather_data['name']}, {weather_data['sys']['country']}"
        temperature = f"**Temperature:** {get_temperature(weather_data)}\N{DEGREE SIGN}F"
        conditions = f"**Conditions:** {weather_data['weather'][0]['description']}"
        humidity = f"**Humidity:** {weather_data['main']['humidity']}%"

        weather = [city, temperature, conditions, humidity]
        formatted_weather = format_weather(weather)
        return formatted_weather
    else:
        return "Sorry, you have entered in the city incorrectly. Please call in this format: \
        !current-weather-bot city OR !current-weather-bot city, country code"

def check_for_error(request):
    """Check if call on OpenWeatherMap was successful or not"""
    if request == {"cod":"404","message":"city not found"}:
        return True
    else:
        return False

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
