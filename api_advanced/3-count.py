#!/usr/bin/python3
"""
Recursively queries the Reddit API, parses titles of all hot articles,
and prints a sorted count of given keywords.
"""
import re
import requests


def count_words(subreddit, word_list, after=None,
                counts=None, first_call=True):
    """Recursively count keyword occurrences in hot post titles.

    Args:
        subreddit (str): the subreddit to search.
        word_list (list): keywords to count (case-insensitive).
        after (str): pagination token for the next page.
        counts (dict): accumulator for word counts, keyed lowercase.
        first_call (bool): tracks the initial call to set up state
            and to print results once recursion completes.
    """
    if first_call:
        counts = {}
        normalized = [word.lower() for word in word_list]
        for word in normalized:
            counts.setdefault(word, 0)

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
        return

    try:
        data = response.json()["data"]
    except (KeyError, ValueError):
        return

    children = data.get("children", [])

    for post in children:
        title = post["data"]["title"].lower()
        tokens = re.findall(r"[a-z0-9']+", title)
        for token in tokens:
            if token in counts:
                counts[token] += 1

    after = data.get("after")
    if after is not None:
        count_words(subreddit, word_list, after, counts, first_call=False)
        return

    if first_call is False:
        return

    results = [(word, cnt) for word, cnt in counts.items() if cnt > 0]
    results.sort(key=lambda pair: (-pair[1], pair[0]))
    for word, cnt in results:
        print("{}: {}".format(word, cnt))
