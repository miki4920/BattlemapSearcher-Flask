import os
import re

from config import CONFIG
from model import BlackListHash


class SubmissionHandler(object):
    @staticmethod
    def check_image_extension(url):
        return url[-3:] not in CONFIG.IMAGE_EXTENSIONS

    @staticmethod
    def check_image_origin(url):
        return not re.search("i\..*\.it", url)

    @staticmethod
    def check_url(submission):
        url = submission["url"]
        if SubmissionHandler.check_image_extension(url):
            return False
        if SubmissionHandler.check_image_origin(url):
            return False
        return True

    @staticmethod
    def check_file_size(submission):
        return CONFIG.MINIMUM_IMAGE_SIZE_IN_BYTES < len(submission) < CONFIG.MAXIMUM_IMAGE_SIZE_IN_BYTES

    @staticmethod
    def check_hash(submission_hash):
        return BlackListHash.filter_by(hash=submission_hash).first() is not None

    @staticmethod
    def get_name(name):
        name = name.lower()
        name = re.sub(r"[^a-zA-Z_]", "_", name)
        name = re.sub(r"_+", "_", name)
        name = name.split("_")
        name = filter(lambda word: len(word) >= 3 and word not in CONFIG.STOP_WORDS, name)
        name = re.sub(r"_+", "_", name)
        name = re.sub("_$|^_", "", name)
        while len(name) > CONFIG.MAXIMUM_NAME_LENGTH:
            name = "_".join(name.split("_")[:-1])
        if len(name) <= 3:
            name = "review"
        return name

    @staticmethod
    def get_extension(url):
        return url[-3:]

    @staticmethod
    def get_path(name, extension):
        unique_name = name
        path = CONFIG.UPLOAD_DIRECTORY + unique_name + "." + extension
        count = 2
        while os.path.exists(path):
            unique_name = name + f"_{count}"
            path = CONFIG.UPLOAD_DIRECTORY + unique_name + "." + extension
            count += 1
        return unique_name, path

    @staticmethod
    def get_square_size(image_name):
        image_name = re.sub("[^a-zA-Z0-9]", "", image_name)
        size = re.search("((?<!\d)\d{1,3}(?!\d))x((?<!\d)\d{1,3}(?!\d))", image_name)
        if not size:
            return None, None
        size = size.group(0)
        size = size.split("x")
        size = [int(number) for number in size]
        return size
