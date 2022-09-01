import requests
import time

import urllib3.exceptions


def get_api_url(subreddit, timestamp):
    return "http://api.pushshift.io/reddit/search/submission/" + f"?subreddit={subreddit}" + f"&after={timestamp}&sort=asc&size=500"


def request_file(url, timeout=0):
    try:
        request = requests.get(url)
        time.sleep(timeout)
        if request.status_code == 200:
            return request
        return None
    except:
        return None