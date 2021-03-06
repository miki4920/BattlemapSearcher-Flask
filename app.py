import os


from flask import render_template, request, send_from_directory, make_response
from random import randint

from config import CONFIG, app
from model import *


@app.get("/")
def main():
    tags = request.args.get("tags", "")
    tags = process_tags(tags)
    page = request.args.get("page", "1")
    page = int(page) if page.isnumeric() else 1
    seed = int(request.cookies.get("seed")) if request.cookies.get("seed") else randint(1, 10000)
    maps = query_maps(tags, seed) if tags else Map.query.order_by(func.rand(seed)).all()
    next_page = page + 1 if (page + 1) * CONFIG.MAPS_PER_PAGE <= len(maps) else False
    previous_page = page - 1 if page >= 1 else False
    maps = maps[(page - 1) * CONFIG.MAPS_PER_PAGE:page * CONFIG.MAPS_PER_PAGE]
    response = make_response(render_template("main.html", maps=maps, tags=request.args.get("tags", ""),
                                             previous_page=previous_page, next_page=next_page))
    response.set_cookie("seed", str(seed))
    return response


@app.get("/maps/<map_id>")
def get_map(map_id):
    battlemap = Map.query.filter_by(id=map_id).first_or_404()
    battlemap_dictionary = battlemap.__dict__
    battlemap_dictionary["tags"] = ",".join([str(tag) for tag in battlemap.tags])
    del battlemap_dictionary["_sa_instance_state"]
    return battlemap_dictionary


@app.get("/maps/<map_id>/download")
def get_map_image(map_id):
    battlemap = Map.query.filter_by(id=map_id).first_or_404()
    path = battlemap.name + "." + battlemap.extension
    return send_from_directory(CONFIG.UPLOAD_DIRECTORY, path=path, as_attachment=True)


@app.route("/maps/<map_id>", methods=["DELETE"])
def delete_map(map_id):
    battlemap = Map.query.filter_by(id=map_id).first_or_404()
    os.remove(battlemap.path)
    os.remove(battlemap.thumbnail_path)
    blacklist = BlackListHash(hash=battlemap.hash)
    db.session.add(blacklist)
    db.session.delete(battlemap)
    db.session.commit()
    return "Valid", 200


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    db.create_all()
    db.session.commit()
    app.run()
