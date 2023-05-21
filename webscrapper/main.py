import json

from sqlalchemy import desc

from model import Map, CONFIG
from network import get_api_url, request_file
from post import Post


def get_timestamp(subreddit):
    newest_map = Map.query.filter_by(subreddit=subreddit).order_by(desc(Map.timestamp)).first()
    return newest_map.timestamp if newest_map is not None else 0


def scrapper():
    for subreddit in CONFIG.SUBREDDITS:
        timestamp = get_timestamp(subreddit)
        while True:
            url = get_api_url(subreddit, timestamp)
            json_data = request_file(url, timeout=1)
            if json_data is None:
                timestamp += 1000
                continue
            try:
                json_data = json_data.json().get("data", [])
            except json.JSONDecodeError:
                print("PushshiftAPI is down. You can check it what's happening with it at the following link: ", url)
                quit()
            if len(json_data) < 1:
                break
            for post_data in json_data:
                post = Post(post_data)
                if post.valid:
                    post.save()
            timestamp = json_data[-1]["created_utc"] + 1


if __name__ == "__main__":
    CONFIG.db.create_all()
    scrapper()