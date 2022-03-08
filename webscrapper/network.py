import socket

import requests
import time


def get_api_url(subreddit, timestamp):
    return "http://api.pushshift.io/reddit/search/submission/" + f"?subreddit={subreddit}" + f"&after={timestamp}&sort=asc&size=1000"


def request_file(url, timeout=0):
    try:
        request = requests.get(url)
    except Exception as e:
        return None
    time.sleep(timeout)
    return request
