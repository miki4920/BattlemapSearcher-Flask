import os


from flask import render_template, request, send_from_directory, make_response
from random import randint

from config import CONFIG
from model import *


@CONFIG.app.get("/")
def main():
    get_tags()
    user_input = request.args.get("user_input", "")
    user_input = process_tags(user_input)
    page = request.args.get("page", "1")
    page = int(page) if page.isnumeric() else 1
    seed = int(request.cookies.get("seed")) if request.cookies.get("seed") else randint(1, 10000)
    maps = query_maps(user_input, seed) if user_input else Map.query.order_by(func.rand(seed)).all()
    next_page = page + 1 if (page + 1) * CONFIG.MAPS_PER_PAGE <= len(maps) else False
    previous_page = page - 1 if page >= 1 else False
    maps = maps[(page - 1) * CONFIG.MAPS_PER_PAGE:page * CONFIG.MAPS_PER_PAGE]
    response = make_response(render_template("main.html", maps=maps, user_input=request.args.get("tags", ""),
                                             previous_page=previous_page, next_page=next_page, tags=[]))
    response.set_cookie("seed", str(seed))
    return response


@CONFIG.app.get("/maps/<map_id>")
def get_map(map_id):
    battlemap = Map.query.filter_by(id=map_id).first_or_404()
    battlemap_dictionary = battlemap.__dict__
    battlemap_dictionary["tags"] = ",".join([str(tag) for tag in battlemap.tags])
    del battlemap_dictionary["_sa_instance_state"]
    return battlemap_dictionary


@CONFIG.app.get("/maps/<map_id>/download")
def get_map_image(map_id):
    battlemap = Map.query.filter_by(id=map_id).first_or_404()
    path = battlemap.image_hash + "." + battlemap.extension
    return send_from_directory(CONFIG.IMAGE_DIRECTORY, path=path, as_attachment=True)


@CONFIG.app.route("/maps/<map_id>", methods=["DELETE"])
def delete_map(map_id):
    battlemap = Map.query.filter_by(id=map_id).first_or_404()
    try:
        os.remove(battlemap.image_path)
        os.remove(battlemap.thumbnail_path)
    except FileNotFoundError:
        pass
    if BlackListHash.query.filter_by(image_hash=battlemap.image_hash).first() is None:
        blacklist = BlackListHash(image_hash=battlemap.image_hash)
        CONFIG.db.session.add(blacklist)
    CONFIG.db.session.delete(battlemap)
    CONFIG.db.session.commit()
    return "Valid", 200


@CONFIG.app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    CONFIG.app.run()
