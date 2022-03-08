import json

from io import BytesIO

from image import image_hash, image_thumbnail, image_dimensions
from model import *
from network import get_api_url, request_file
from submission_handler import SubmissionHandler


class WebScrapper(object):
    def get_submission(self, submission):
        name = submission["title"]
        extension = submission["url"][-3:].lower()
        image = request_file(submission["url"], timeout=1)
        if image is None:
            return
        image = image.content
        dimensions = image_dimensions(BytesIO(image))
        if dimensions is None:
            return
        width, height = dimensions.size
        if width < CONFIG.MINIMUM_IMAGE_DIMENSION and height < CONFIG.MINIMUM_IMAGE_DIMENSION:
            return
        square_width, square_height = SubmissionHandler.get_square_size(name)
        battlemap_hash = image_hash(BytesIO(image))
        name = SubmissionHandler.get_name(submission)
        name = SubmissionHandler.get_path(name, extension)
        path = name + "." + extension
        if Map.query.filter_by(hash=battlemap_hash).first() is None and Map.query.filter_by(
                path=CONFIG.UPLOAD_DIRECTORY + path).first() is None:
            with open("../" + CONFIG.UPLOAD_DIRECTORY + path, "wb") as file:
                file.write(image)
            image_thumbnail("../" + CONFIG.UPLOAD_DIRECTORY + path, "../" + CONFIG.THUMBNAIL_DIRECTORY + path, extension)
            create_map(name=name, extension=extension, path=path, width=width, height=height, square_width=square_width,
                       square_height=square_height, hash=battlemap_hash)

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
                        if SubmissionHandler.check_url(submission):
                            self.get_submission(submission)
                    timestamp = int(json_data[-1]["created_utc"])
                except json.decoder.JSONDecodeError:
                    timestamp += 1000


if __name__ == "__main__":
    webscrapper = WebScrapper()
    webscrapper.scrapper()