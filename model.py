import re

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

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
    path = db.Column(db.String(CONFIG.MAXIMUM_NAME_LENGTH * 10))
    thumbnail_path = db.Column(db.String(CONFIG.MAXIMUM_NAME_LENGTH * 2))
    width = db.Column(db.INTEGER)
    height = db.Column(db.INTEGER)
    square_width = db.Column(db.INTEGER, nullable=True)
    square_height = db.Column(db.INTEGER, nullable=True)
    tags = db.relationship("Tag", secondary=tags_table,
                           backref=db.backref("maps"))


def query_maps_by_name(tags, seed):
    tags = [Map.name.contains(tag) for tag in tags]
    maps = Map.query.filter(*tags).order_by(func.rand(seed))
    return list(maps) if maps is not None else []


def query_maps_by_tags(tags, seed):
    tags = ",".join(tags)
    maps = Map.query.from_statement(db.text(f"""SELECT map_id FROM 
    (SELECT map_id, GROUP_CONCAT(tag_id ORDER BY tag_id) 
    AS tag_id FROM tags GROUP BY map_id) as t where tag_id LIKE \"%%{tags}%%\" ORDER BY RAND({seed})""")).all()
    return list(maps) if maps else []


def query_maps(tags, seed):
    maps = query_maps_by_name(tags, seed) + query_maps_by_tags(tags, seed)
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


def create_map(**kwargs):
    name = kwargs.get("name")
    extension = kwargs.get("extension")
    path = kwargs.get("path")
    width, height = kwargs.get("width"), kwargs.get("height")
    square_width, square_height = kwargs.get("square_width"), kwargs.get("square_height")
    battlemap_hash = kwargs.get("hash")
    image_path = CONFIG.UPLOAD_DIRECTORY + path
    thumbnail_path = CONFIG.THUMBNAIL_DIRECTORY + path
    battlemap = Map(name=name, extension=extension, hash=battlemap_hash, path=image_path,
                    thumbnail_path=thumbnail_path,
                    width=width, height=height, square_width=square_width, square_height=square_height)
    tags = name.split(" ")
    for tag in tags:
        if len(tag) < CONFIG.MINIMUM_NAME_LENGTH:
            continue
        query_tag = Tag.query.filter_by(id=tag).first()
        if query_tag is None:
            query_tag = Tag(id=tag)
        if str(query_tag) not in list(map(str, battlemap.tags)):
            battlemap.tags.append(query_tag)
    db.session.add(battlemap)
    db.session.commit()