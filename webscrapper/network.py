import time

import requests


def get_api_url(subreddit, timestamp):
    return "http://api.pushshift.io/reddit/search/submission/" + f"?subreddit={subreddit}" + f"&after={timestamp}&size=500&order=asc"


def request_file(url, timeout=0):
    try:
        request = requests.get(url, timeout=10)
        time.sleep(timeout)
        if request.status_code == 200:
            return request
        return None
    except Exception as e:
        print(url)
        print("API does not work!")
        quit()