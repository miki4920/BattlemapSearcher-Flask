import os
import io

from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from PIL import Image

from config import CONFIG
from errors import ValidationError
from getting import *
from validation import validate_battlemap

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'mysql://{os.getenv("USERNAME")}:{os.getenv("PASSWORD")}@{os.getenv("IP")}/flask'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

tags_table = db.Table('tags', db.Column('tag_id', db.String(CONFIG.MAXIMUM_NAME_LENGTH),
                      db.ForeignKey('tag.id'), primary_key=True),
                      db.Column('map_id', db.Integer,
                      db.ForeignKey('map.id'), primary_key=True))


class Tag(db.Model):
    id = db.Column(db.String(CONFIG.MAXIMUM_NAME_LENGTH), primary_key=True)


class Map(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(CONFIG.MAXIMUM_NAME_LENGTH))
    extension = db.Column(db.String(3))
    hash = db.Column(db.String(16))
    path = db.Column(db.String(CONFIG.MAXIMUM_NAME_LENGTH * 2))
    thumbnail_path = db.Column(db.String(CONFIG.MAXIMUM_NAME_LENGTH * 2))
    width = db.Column(db.INTEGER)
    height = db.Column(db.INTEGER)
    square_width = db.Column(db.INTEGER, nullable=True)
    square_height = db.Column(db.INTEGER, nullable=True)
    tags = db.relationship("Tag", secondary=tags_table,
                           backref=db.backref("maps"))


def get_default(value, default):
    return value if value else default


def get_matching(maps, tags):
    map_dictionary = {}
    for battlemap in maps:
        if map_dictionary.get(battlemap) is None:
            map_dictionary[battlemap] = 0
        map_dictionary[battlemap] += 1
    maps = [battlemap for battlemap in map_dictionary if map_dictionary[battlemap] > len(tags)-1]
    return maps


@app.get("/")
def main():
    tags = get_default(request.args.get("tags"), "")
    page = get_default(request.args.get("page"), "1")
    if tags:
        maps = []
        tags = tags.split(" ")
        for tag in tags:
            tag = Tag.query.filter_by(id=tag).first()
            if tag is not None:
                maps.extend(tag.maps)
        maps = get_matching(maps, tags)
    return render_template("main.html")


def save_file(data, file):
    path = get_path(data)
    stream = io.BytesIO(file.stream.read())
    file.save(path)

    thumbnail_path = get_thumbnail_path(data)
    extension = get_extension(data).upper()

    with Image.open(stream) as thumbnail:
        thumbnail = thumbnail.resize((CONFIG.THUMBNAIL_SIZE, CONFIG.THUMBNAIL_SIZE), Image.ANTIALIAS)
        thumbnail.save(thumbnail_path, "JPEG" if extension == "JPG" else extension)


def create_map(data):
    name = get_name(data)
    extension = get_extension(data)
    battlemap_hash = get_hash(data)
    path = get_path(data)
    thumbnail_path = get_thumbnail_path(data)
    width, height = get_dimensions(data)
    square_width, square_height = get_square_dimensions(data)
    battlemap = Map(name=name, extension=extension, hash=battlemap_hash, path=path, thumbnail_path=thumbnail_path,
                    width=width, height=height, square_width=square_width, square_height=square_height)
    return battlemap


@app.post("/maps")
def post_maps():
    data = request.form
    file = request.files["image"]
    try:
        validate_battlemap(data)
        save_file(data, file)
        battlemap = create_map(data)
        if data.get("tags") is not None:
            for tag in data.get("tags").split(","):
                query_tag = Tag.query.filter_by(id=tag).first()
                if query_tag is None:
                    query_tag = Tag(id=tag)
                battlemap.tags.append(query_tag)
        db.session.add(battlemap)
        db.session.commit()
        return "Valid", 200
    except ValidationError as e:
        return e.message, e.error_code
    except Exception as e:
        raise e


if __name__ == "__main__":
    db.create_all()
    db.session.commit()
    app.run()
    app.add_url_rule("/favicon.ico",
                     redirect_to=url_for("static", filename="icons/favicon.ico"))
