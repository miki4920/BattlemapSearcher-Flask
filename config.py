import os

from flask import Flask


class CONFIG:
    MINIMUM_NAME_LENGTH = 3
    MAXIMUM_NAME_LENGTH = 128
    SUBREDDITS = [
        "battlemaps",
        "dndmaps",
        "dungeondraft",
        "fantasymaps",
        "miskasmaps",
        "roll20",
        "FoundryVTT"
    ]
    IMAGE_EXTENSIONS = ["png", "jpg"]
    MINIMUM_IMAGE_SIZE_IN_BYTES = 5000
    MAXIMUM_IMAGE_SIZE_IN_BYTES = 20485760
    STATIC_DIRECTORY = "static"
    REST_DIRECTORY = "maps"
    UPLOAD_DIRECTORY = STATIC_DIRECTORY + "/images"
    MINIMUM_IMAGE_DIMENSION = 100
    THUMBNAIL_SIZE = 512
    THUMBNAIL_DIRECTORY = UPLOAD_DIRECTORY + "/thumbnails"
    MAPS_PER_PAGE = 100


app = Flask(__name__, static_url_path="/" + CONFIG.STATIC_DIRECTORY, static_folder=CONFIG.STATIC_DIRECTORY)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'mysql://{os.getenv("USERNAME")}:{os.getenv("PASSWORD")}@{os.getenv("IP")}/flask'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
