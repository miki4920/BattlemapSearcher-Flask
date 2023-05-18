import os
import re

from io import BytesIO

import PIL
from PIL import Image

from config import CONFIG
from model import BlackListHash, Map, create_map
from webscrapper.network import request_file
from webscrapper.image import image_hash


class Post:
    def __init__(self, submission):
        self.submission = submission
        self.setters = [self.set_author, self.set_name, self.set_url, self.set_extension, self.set_timestamp, self.set_subreddit, self.set_image, self.set_image_hash, self.set_image_thumbnail, self.set_dimensions, self.set_square_dimensions]
        self.valid = True
        self.author = ""
        self.name = ""
        self.extension = ""
        self.subreddit = ""
        self.timestamp = 0
        self.url = ""
        self.image = None
        self.image_hash = ""
        self.thumbnail = None
        self.width = 0
        self.height = 0
        self.square_width = None
        self.square_height = None

        for setter in self.setters:
            setter()
            if not self.valid:
                break

    def set_author(self):
        self.author = self.submission.get("author", self.author)
        if not (CONFIG.MINIMUM_NAME_LENGTH < len(self.author) < CONFIG.MAXIMUM_NAME_LENGTH):
            self.valid = False
            return

    def set_name(self):
        self.name = self.submission.get("title", self.name)
        if not (CONFIG.MINIMUM_NAME_LENGTH < len(self.name) < CONFIG.MAXIMUM_NAME_LENGTH):
            self.valid = False
            return
        self.name = self.name.lower()
        self.name = re.sub(r"[^a-zA-Z]+", " ", self.name)
        self.name = re.sub(r" +", " ", self.name)
        self.name = re.sub(" $|^ ", "", self.name)
        self.name = " ".join([word.capitalize() for word in self.name.split(" ") if len(word) >= 3])

    def set_extension(self):
        url = self.submission["url"].upper()
        self.extension = re.search(r".*\.(JPG|PNG|JPEG)", url)
        if not self.extension:
            self.valid = False
            return
        self.extension = self.extension.group(1).upper()
        self.extension = self.extension if self.extension != "JPG" else "JPEG"

    def set_timestamp(self):
        self.timestamp = self.submission["created_utc"]

    def set_subreddit(self):
        self.subreddit = self.submission["subreddit"]

    def set_url(self):
        self.url = self.submission["url"]
        if not self.url:
            self.valid = False
            return

    def set_image(self):
        self.image = request_file(self.url, timeout=1)
        if self.image is None:
            self.valid = False
            return
        self.image = self.image.content
        if not (CONFIG.MINIMUM_IMAGE_LENGTH < len(self.image) < CONFIG.MAXIMUM_IMAGE_LENGTH):
            self.valid = False
            return
        self.image = BytesIO(self.image)
        try:
            self.image = Image.open(self.image)
        except PIL.UnidentifiedImageError:
            self.valid = False
            return

    def set_image_thumbnail(self):
        self.thumbnail = self.image.resize((CONFIG.THUMBNAIL_SIZE, CONFIG.THUMBNAIL_SIZE), Image.ANTIALIAS)

    def set_image_hash(self):
        self.image_hash = image_hash(self.image)
        if Map.query.filter_by(image_hash=self.image_hash).first() is not None or BlackListHash.query.filter_by(image_hash=self.image_hash).first() is not None:
            self.valid = False
            return

    def set_dimensions(self):
        self.width, self.height = self.image.size

    def set_square_dimensions(self):
        size = re.search(r"((?<!\d)\d{1,2}(?!\d))x((?<!\d)\d{1,2}(?!\d))", self.submission["title"])
        if not size:
            return
        self.square_width = size.group(1)
        self.square_height = size.group(2)

    def save(self):
        file_name = f"{self.image_hash}.{self.extension}"
        image_path = os.path.join(CONFIG.IMAGE_DIRECTORY, file_name)
        thumbnail_path = os.path.join(CONFIG.THUMBNAIL_DIRECTORY, file_name)
        self.image = self.image.convert("RGB")
        self.thumbnail = self.thumbnail.convert("RGB")
        self.image.save(os.path.join(os.path.dirname(CONFIG.app.instance_path), image_path))
        self.thumbnail.save(os.path.join(os.path.dirname(CONFIG.app.instance_path), thumbnail_path))
        create_map(vars(self), image_path, thumbnail_path)

