#!/usr/bin/python3
"""
Recursively queries the Reddit API and returns a list of titles
of all hot articles for a given subreddit.
"""
import requests


def recurse(subreddit, hot_list=[], after=None, first_call=True):
    """Recursively collect hot post titles for a subreddit.

    Args:
        subreddit (str): the subreddit to search.
        hot_list (list): accumulator list of titles.
        after (str): pagination token for the next page.
        first_call (bool): tracks whether this is the initial call,
            so hot_list can be reset between separate top-level calls.

    Returns:
        list of titles, or None if the subreddit is invalid.
    """
    if first_call:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        "User-Agent": "linux:alche-api-advanced:v1.0 (by /u/shania178)"
    }
    params = {"limit": 100, "after": after}

    response = requests.get(
        url,
        headers=headers,
        params=params,
        allow_redirects=False
    )

    if response.status_code != 200:
        return None

    try:
        data = response.json()["data"]
    except (KeyError, ValueError):
        return None

    children = data.get("children", [])
    if not children and first_call:
        return None

    for post in children:
        hot_list.append(post["data"]["title"])

    after = data.get("after")
    if after is None:
        return hot_list

    return recurse(subreddit, hot_list, after, first_call=False)
