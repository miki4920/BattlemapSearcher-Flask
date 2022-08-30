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
            json_data = request_file(url)
            if json_data is None:
                timestamp += 1000
                continue
            json_data = json_data.json().get("data", [])
            if len(json_data) < 1:
                break
            for post_data in json_data:
                post = Post(post_data)
                if post.valid:
                    post.save()
            timestamp = json_data[-1]["created_utc"]


if __name__ == "__main__":
    CONFIG.db.create_all()
    scrapper()