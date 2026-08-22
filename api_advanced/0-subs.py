#!/usr/bin/python3
"""
Queries the Reddit API and returns the number of
subscribers for a given subreddit.
"""


import requests


def number_of_subscribers(subreddit):
    """Return the number of subscribers for a subreddit."""
    base_url = "https://www.reddit.com/r/{}/about.json".format(subreddit)

    headers = {
        "User-Agent": "alche-api-advanced/1.0"
    }

    response = requests.get(
        base_url,
        headers=headers,
        allow_redirects=False
    )
    if response.status_code != 200:
        return 0
    try:
        data = response.json()
        return data["data"]["subscribers"]
    except(KeyError, ValueError, TypeError):
        return 0
