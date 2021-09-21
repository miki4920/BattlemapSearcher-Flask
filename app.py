from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy

from config import CONFIG

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('map_id', db.Integer, db.ForeignKey('map.id'), primary_key=True)
)


class Tag(db.Model):
    id = db.column(db.String(CONFIG.MAXIMUM_NAME_LENGTH), primary_key=True)



class Map(db.Model):
    id = db.column(db.INTEGER, primary_key=True)
    name = db.column(db.String(CONFIG.MAXIMUM_NAME_LENGTH))
    extension = db.column(db.String(3))
    hash = db.column(db.String(16))
    path = db.column(db.String(CONFIG.MAXIMUM_NAME_LENGTH*2))
    width = db.column(db.INTEGER)
    height = db.column(db.INTEGER)
    square_width = db.column(db.INTEGER, nullable=True)
    square_height = db.column(db.INTEGER, nullable=True)
    uploader = db.column(db.String(CONFIG.MAXIMUM_NAME_LENGTH))
    tags = db.relationship("Tag", secondary=tags, lazy="subquery",
                           backref=db.backref("maps"))


def get_default(value, default):
    return value if value else default


@app.route("/")
def main():
    tags = get_default(request.args.get("tags"), "")
    page = get_default(request.args.get("page"), "1")
    return render_template("main.html")


if __name__ == '__main__':
    app.run()
    app.add_url_rule("/favicon.ico",
                     redirect_to=url_for("static", filename="icons/favicon.ico"))
