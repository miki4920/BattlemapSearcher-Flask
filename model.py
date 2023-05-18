import re

from sqlalchemy import func

from config import CONFIG

tags_table = CONFIG.db.Table('tags', CONFIG.db.Column('tag_id', CONFIG.db.String(CONFIG.MAXIMUM_NAME_LENGTH),
                                                      CONFIG.db.ForeignKey('tag.id'), primary_key=True),
                             CONFIG.db.Column('map_id', CONFIG.db.Integer,
                                              CONFIG.db.ForeignKey('map.id'), primary_key=True))


class BlackListHash(CONFIG.db.Model):
    image_hash = CONFIG.db.Column(CONFIG.db.String(16), primary_key=True)

    def __str__(self):
        return self.hash


class BlackListWord(CONFIG.db.Model):
    word = CONFIG.db.Column(CONFIG.db.String(CONFIG.MAXIMUM_NAME_LENGTH), primary_key=True)

    def __str__(self):
        return self.word


class StopWordList(CONFIG.db.Model):
    word = CONFIG.db.Column(CONFIG.db.String(CONFIG.MAXIMUM_NAME_LENGTH), primary_key=True)

    def __str__(self):
        return self.word


class Tag(CONFIG.db.Model):
    id = CONFIG.db.Column(CONFIG.db.String(CONFIG.MAXIMUM_NAME_LENGTH), primary_key=True)

    def __str__(self):
        return self.id


class Map(CONFIG.db.Model):
    id = CONFIG.db.Column(CONFIG.db.INTEGER, primary_key=True)
    author = CONFIG.db.Column(CONFIG.db.String(CONFIG.MAXIMUM_NAME_LENGTH))
    name = CONFIG.db.Column(CONFIG.db.String(CONFIG.MAXIMUM_NAME_LENGTH))
    extension = CONFIG.db.Column(CONFIG.db.String(4))
    timestamp = CONFIG.db.Column(CONFIG.db.INTEGER)
    subreddit = CONFIG.db.Column(CONFIG.db.String(CONFIG.MAXIMUM_NAME_LENGTH))
    image_path = CONFIG.db.Column(CONFIG.db.String(CONFIG.MAXIMUM_NAME_LENGTH))
    image_hash = CONFIG.db.Column(CONFIG.db.String(16), unique=True)
    thumbnail_path = CONFIG.db.Column(CONFIG.db.String(CONFIG.MAXIMUM_NAME_LENGTH))
    width = CONFIG.db.Column(CONFIG.db.INTEGER)
    height = CONFIG.db.Column(CONFIG.db.INTEGER)
    square_width = CONFIG.db.Column(CONFIG.db.INTEGER, nullable=True)
    square_height = CONFIG.db.Column(CONFIG.db.INTEGER, nullable=True)
    tags = CONFIG.db.relationship("Tag", secondary=tags_table,
                                  backref=CONFIG.db.backref("maps"))


def query_maps_by_name(tags, seed):
    tags = [Map.name.contains(tag) for tag in tags]
    maps = Map.query.filter(*tags).order_by(func.rand(seed))
    return list(maps) if maps is not None else []


def query_maps_by_tags(tags, seed):
    tags = ",".join(tags)
    maps = Map.query.from_statement(CONFIG.db.text(f"""SELECT map_id FROM 
    (SELECT map_id, GROUP_CONCAT(tag_id ORDER BY tag_id) 
    AS tag_id FROM tags GROUP BY map_id) as t where tag_id LIKE \"%%{tags}%%\" ORDER BY RAND({seed})""")).all()
    return list(maps) if maps else []


def query_maps_by_author(tags, seed):
    tags = [Map.author.contains(tag) for tag in tags]
    maps = Map.query.filter(*tags).order_by(func.rand(seed))
    return list(maps) if maps is not None else []


def query_maps(tags, seed):
    maps = query_maps_by_name(tags, seed) + query_maps_by_author(tags, seed) + query_maps_by_tags(tags, seed)
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


def create_map(post_dictionary, image_path, thumbnail_path):
    battlemap = Map(author=post_dictionary["author"], name=post_dictionary["name"], extension=post_dictionary["extension"],
                    timestamp=post_dictionary["timestamp"], subreddit=post_dictionary["subreddit"], image_path=image_path,
                    image_hash=post_dictionary["image_hash"], thumbnail_path=thumbnail_path,
                    width=post_dictionary["width"], height=post_dictionary["height"],
                    square_width=post_dictionary["square_width"], square_height=post_dictionary["square_height"])
    tags = post_dictionary["name"].split(" ")
    for tag in tags:
        if len(tag) < CONFIG.MINIMUM_NAME_LENGTH:
            continue
        query_tag = Tag.query.filter_by(id=tag).first()
        if query_tag is None:
            query_tag = Tag(id=tag)
        if str(query_tag) not in list(map(str, battlemap.tags)):
            battlemap.tags.append(query_tag)
    CONFIG.db.session.add(battlemap)
    CONFIG.db.session.commit()
