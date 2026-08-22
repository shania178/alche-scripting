#!/usr/bin/python3
"""
Queries the Reddit API and prints the titles of the first
10 hot posts listed for a given subreddit.
"""

import requests


def top_ten(subreddit):
    """Print the titles of first 10 hot posts."""
    base_url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        "User-Agent": "alche-api-advanced/1.0"
    }

    response = requests.get(
        base_url,
        headers=headers,
        allow_redirects=False
    )

    if response.status_code != 200:
        print(None)
        return

    data = response.json()
    posts = data["data"]["children"]

    for post in posts[:10]:
        print(post["data"]["title"])
