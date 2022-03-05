import json
import os
import re

from io import BytesIO
from PIL import Image

from config import CONFIG
from hash import hash_image
from model import *
from network import get_api_url, request_file
from submission_handler import SubmissionHandler


class WebScrapper(object):
    def get_submission(self, submission):
        if SubmissionHandler.check_url(submission):
            name = SubmissionHandler.get_name(submission)

            submission = request_file(submission_dictionary["url"], timeout=1).content
            submission_dictionary["width"], submission_dictionary["height"] = Image.open(BytesIO(submission)).size
            submission_dictionary["hash"] = hash_image(submission)
            if self.check_file_size(submission) and submission_dictionary["hash"] not in self.hash_set:
                write_file(submission_dictionary["path"], submission)
                self.submission_list.append(submission_dictionary)
                self.hash_set.add(submission_dictionary["hash"])

    def scrapper(self):
        for subreddit in CONFIG.SUBREDDITS:
            timestamp = 0
            while True:
                url = get_api_url(subreddit, timestamp)
                try:
                    json_data = request_file(url)
                    json_data = json_data.json()["data"]
                    if len(json_data) < 1:
                        break
                    for submission in json_data:
                        print(submission)
                    timestamp = int(json_data[-1]["created_utc"])
                except json.decoder.JSONDecodeError:
                    timestamp += 1000


if __name__ == "__main__":
    webscrapper = WebScrapper()
    webscrapper.scrapper()