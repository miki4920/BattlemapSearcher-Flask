import io
import re

from flask_sqlalchemy import SQLAlchemy
from PIL import Image

from config import app, CONFIG

db = SQLAlchemy(app)

tags_table = db.Table('tags', db.Column('tag_id', db.String(CONFIG.MAXIMUM_NAME_LENGTH),
                                        db.ForeignKey('tag.id'), primary_key=True),
                      db.Column('map_id', db.Integer,
                                db.ForeignKey('map.id'), primary_key=True))


class Tag(db.Model):
    id = db.Column(db.String(CONFIG.MAXIMUM_NAME_LENGTH), primary_key=True)

    def __str__(self):
        return self.id


class BlackListHash(db.Model):
    hash = db.Column(db.String(16), primary_key=True)

    def __str__(self):
        return self.hash


class StopWordList(db.Model):
    word = db.Column(db.String(CONFIG.MAXIMUM_NAME_LENGTH), primary_key=True)

    def __str__(self):
        return self.word


class Map(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(CONFIG.MAXIMUM_NAME_LENGTH))
    extension = db.Column(db.String(3))
    hash = db.Column(db.String(16), unique=True)
    path = db.Column(db.String(CONFIG.MAXIMUM_NAME_LENGTH * 2))
    thumbnail_path = db.Column(db.String(CONFIG.MAXIMUM_NAME_LENGTH * 2))
    width = db.Column(db.INTEGER)
    height = db.Column(db.INTEGER)
    square_width = db.Column(db.INTEGER, nullable=True)
    square_height = db.Column(db.INTEGER, nullable=True)
    tags = db.relationship("Tag", secondary=tags_table,
                           backref=db.backref("maps"))


def save_file(data, file):
    path = get_path(data)
    thumbnail_path = get_thumbnail_path(data)
    stream = file.stream.read()
    extension = get_extension(data).upper()

    with open(path, "wb") as file:
        file.write(stream)

    with Image.open(io.BytesIO(stream)) as thumbnail:
        thumbnail = thumbnail.resize((CONFIG.THUMBNAIL_SIZE, CONFIG.THUMBNAIL_SIZE), Image.ANTIALIAS)
        thumbnail.save(thumbnail_path, "JPEG" if extension == "JPG" else extension)


def query_maps_by_name(tags):
    tags = [Map.name.contains(tag) for tag in tags]
    maps = Map.query.filter(*tags)
    return maps if maps is not None else []


def query_maps_by_tags(tags):
    tags = ",".join(tags)
    maps = Map.query.from_statement(db.text(f"""SELECT map_id FROM 
    (SELECT map_id, GROUP_CONCAT(tag_id ORDER BY tag_id) 
    AS tag_id FROM tags GROUP BY map_id) as t where tag_id LIKE \"%%{tags}%%\" """)).all()
    return maps if maps else []


def query_maps(tags):
    maps = query_maps_by_name(tags) + query_maps_by_tags(tags)
    maps = list(dict.fromkeys(maps))
    return maps


def process_tags(tags):
    if not tags:
        return ""
    tags = tags.lower()
    tags = re.sub("[^a-z ]", " ", tags)
    tags = re.sub(" +", " ", tags)
    tags = tags.strip(" ")
    return tags.split(" ")
