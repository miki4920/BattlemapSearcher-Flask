import requests
import time


def get_api_url(subreddit, timestamp):
    return "http://api.pushshift.io/reddit/search/submission/" + f"?subreddit={subreddit}" + f"&after={timestamp}&sort=asc&size=1000"


def request_file(url, timeout=0):
    request = requests.get(url)
    time.sleep(timeout)
    return request
