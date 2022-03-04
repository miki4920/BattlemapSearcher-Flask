import json
import re

from io import BytesIO
from PIL import Image

from config import CONFIG
from model import *
from network import get_api_url, request_file


class WebScrapper(object):
    @staticmethod
    def image_format(submission):
        return submission["url"][-3:] not in CONFIG.IMAGE_EXTENSIONS

    @staticmethod
    def blacklist_word(submission):
        image_name = submission["title"].lower()
        return any([BlackListWord.filter_by(word=word).first() is not None for word in image_name])

    def check_title(self, submission):
        url = submission["url"][-3:]
        if self.image_format(url):
            return False
        if self.blacklist_word(submission):
            return False
        return True

    @staticmethod
    def check_file_size(submission):
        return CONFIG.MINIMUM_IMAGE_SIZE_IN_BYTES < len(submission) < CONFIG.MAXIMUM_IMAGE_SIZE_IN_BYTES

    @staticmethod
    def blacklist_hash(submission_hash):
        return BlackListHash.filter_by(hash=submission_hash).first() is not None

    def get_submission(self, submission):
        if self.check_title(submission):
            submission_dictionary = self.dictionary_maker(submission, submission["created_utc"])
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
                    json_data = request_file(url).json()["data"]
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