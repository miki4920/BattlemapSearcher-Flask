import os
import io

from flask import Flask, render_template, url_for, request, send_from_directory, abort
from flask_sqlalchemy import SQLAlchemy
from PIL import Image

from config import CONFIG
from errors import ValidationError
from getting import *
from validation import validate_battlemap

app = Flask(__name__, static_url_path="/" + CONFIG.STATIC_DIRECTORY, static_folder=CONFIG.STATIC_DIRECTORY)
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
    else:
        maps = Map.query.limit(CONFIG.MAPS_PER_PAGE).all()
    return render_template("main.html", maps=maps)


@app.get("/maps")
def get_maps():
    maps = Map.query.all()
    return render_template("get.html", maps=maps)


@app.get("/maps/<map_id>")
def get_map(map_id):
    battlemap = Map.query.filter_by(id=map_id).first()
    if battlemap is None:
        return abort(404)
    battlemap = battlemap.__dict__
    del battlemap["_sa_instance_state"]
    battlemap["path"] = url_for(".get_map_image", map_id=battlemap["id"])
    return battlemap


@app.get("/maps/<map_id>/download")
def get_map_image(map_id):
    battlemap = Map.query.filter_by(id=map_id).first()
    if battlemap is None:
        return abort(404)
    path = battlemap.name + "." + battlemap.extension
    return send_from_directory(CONFIG.UPLOAD_DIRECTORY, path=path, as_attachment=True)


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
def post_map():
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


@app.route("/maps/<map_id>", methods=["DELETE"])
def delete_map(map_id):
    battlemap = Map.query.filter_by(id=map_id).first()
    if battlemap:
        db.session.delete(battlemap)
        db.session.commit()
        return "Valid", 200
    abort(404)


if __name__ == "__main__":
    db.create_all()
    db.session.commit()
    app.run()
    app.add_url_rule("/favicon.ico",
                     redirect_to=url_for("static", filename="icons/favicon.ico"))
