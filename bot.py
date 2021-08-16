import praw
import config
import requests

reddit = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    weather_api = config.weather_api,
                    user_agent = "current-weather-bot v0.0.1")

reddit.validate_on_submit=True

subreddit = reddit.subreddit("test")

# make a post on "test" subreddit
subreddit.submit("Test Submission", url="https://reddit.com")

# get full weather url
weather_url = "http://api.openweathermap.org/data/2.5/weather?"
full_url = weather_url + f"q=Seattle&appid={config.weather_api}"

# have bot respond to comments with its name
for comment in subreddit.stream.comments():
    if comment.body.startswith("!current-weather-bot"):
        weather_request = requests.get(full_url)
        comment.reply(weather_request)