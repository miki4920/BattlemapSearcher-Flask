from flask import Flask, render_template, url_for, request, make_response
from flask_sqlalchemy import SQLAlchemy

from config import CONFIG
from errors import ValidationError
from validation import validate_battlemap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

tags_table = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('map_id', db.Integer, db.ForeignKey('map.id'), primary_key=True)
                )


class Tag(db.Model):
    id = db.Column(db.String(CONFIG.MAXIMUM_NAME_LENGTH), primary_key=True)


class Map(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(CONFIG.MAXIMUM_NAME_LENGTH))
    extension = db.Column(db.String(3))
    hash = db.Column(db.String(16))
    path = db.Column(db.String(CONFIG.MAXIMUM_NAME_LENGTH * 2))
    width = db.Column(db.INTEGER)
    height = db.Column(db.INTEGER)
    square_width = db.Column(db.INTEGER, nullable=True)
    square_height = db.Column(db.INTEGER, nullable=True)
    uploader = db.Column(db.String(CONFIG.MAXIMUM_NAME_LENGTH))
    tags = db.relationship("Tag", secondary=tags_table,
                           backref=db.backref("maps"))


def get_default(value, default):
    return value if value else default


@app.get("/")
def main():
    tags = get_default(request.args.get("tags"), "")
    page = get_default(request.args.get("page"), "1")
    return render_template("main.html")


if __name__ == '__main__':
    app.run()
    app.add_url_rule("/favicon.ico",
                     redirect_to=url_for("static", filename="icons/favicon.ico"))


@app.post("/maps")
def post_maps():
    data = request.form
    file = request.files["image"]
    try:
        validate_battlemap(data)
        return "Valid", 200
    except ValidationError as e:
        return e.message, e.error_code
    except Exception as e:
        raise e
