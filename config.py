import os
from PIL import Image

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class CONFIG:
    MINIMUM_NAME_LENGTH = 3
    MAXIMUM_NAME_LENGTH = 512
    SUBREDDITS = [
        "battlemaps",
        "dndmaps",
        "dungeondraft",
        "fantasymaps",
        "miskasmaps",
        "roll20",
        "FoundryVTT"
    ]
    MINIMUM_IMAGE_LENGTH = 104857
    MAXIMUM_IMAGE_LENGTH = 20971520
    STATIC_DIRECTORY = "static"
    IMAGE_DIRECTORY = os.path.join(STATIC_DIRECTORY, "maps")
    THUMBNAIL_SIZE = 512
    THUMBNAIL_DIRECTORY = os.path.join(STATIC_DIRECTORY, "thumbnails")
    MAPS_PER_PAGE = 100
    Image.MAX_IMAGE_PIXELS = 933120000
    app = Flask(__name__, static_url_path="/" + STATIC_DIRECTORY, static_folder=STATIC_DIRECTORY)
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'mysql://{os.getenv("USERNAME")}:{os.getenv("PASSWORD")}@{os.getenv("IP")}/{os.getenv("SCHEMA_NAME")}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db = SQLAlchemy(app)



