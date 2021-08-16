import praw
import config

reddit = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    user_agent = "current-weather-bot v0.0.1")

reddit.validate_on_submit=True

subreddit = reddit.subreddit("test")

subreddit.submit("Test Submission", url="https://reddit.com")