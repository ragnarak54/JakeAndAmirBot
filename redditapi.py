import praw
import config


def read_script(link):
    reddit = praw.Reddit(client_id=config.reddit_id,
                         client_secret=config.reddit_secret,
                         user_agent=config.reddit_id + config.reddit_username,
                         username=config.reddit_username,
                         password=config.reddit_password)

    script_submission = reddit.submission(url=link)

    if script_submission == "[deleted]":
        return ""
    else:
        return script_submission.selftext
