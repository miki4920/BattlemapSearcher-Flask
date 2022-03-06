import os
import re
import requests

from io import BytesIO
from zipfile import ZipFile

from config import CONFIG
from image import image_hash, image_thumbnail, image_dimensions
from model import Map, Tag, db


class PatreonScrapper(object):
    def __init__(self):
        self.url = CONFIG.STARTING_URL

    @staticmethod
    def get_name(name):
        if re.match("[A-Z0-9][A-Z0-9]", name[-2:]):
            return name[:-2]
        return name

    @staticmethod
    def create_map(path):
        name, extension = path[:-4], path[-3:]
        battlemap_hash = image_hash("../" + CONFIG.UPLOAD_DIRECTORY + path)
        image_thumbnail("../" + CONFIG.UPLOAD_DIRECTORY + path, "../" + CONFIG.THUMBNAIL_DIRECTORY + path, extension)
        image_path = CONFIG.UPLOAD_DIRECTORY + path
        thumbnail_path = CONFIG.THUMBNAIL_DIRECTORY + path
        width, height = image_dimensions("../" + CONFIG.UPLOAD_DIRECTORY + path)
        square_width, square_height = width//140, height//140
        name = PatreonScrapper.get_name(name)
        if Map.query.filter_by(hash=battlemap_hash).first() is not None:
            return
        battlemap = Map(name=name, extension=extension, hash=battlemap_hash, path=image_path, thumbnail_path=thumbnail_path,
                        width=width, height=height, square_width=square_width, square_height=square_height)
        tags = name.split(" ")
        for tag in tags:
            query_tag = Tag.query.filter_by(id=tag).first()
            if query_tag is None:
                query_tag = Tag(id=tag)
            if str(query_tag) not in list(map(str, battlemap.tags)):
                battlemap.tags.append(query_tag)
        db.session.add(battlemap)
        db.session.commit()

    @staticmethod
    def download(url):
        download = requests.get(url, cookies=CONFIG.COOKIES)
        if download.status_code != 200:
            return
        with ZipFile(BytesIO(download.content)) as download_zip:
            for file_name in download_zip.namelist():
                if re.match("^(?!__MACOSX).+GL_.+\.(jpg|png)", file_name):
                    path = re.search("GL_.+\.(jpg|png)", file_name).group(0)
                    path = "".join(path.split("_"))
                    path = re.split("([A-Z][a-z]+)", path)
                    path = [word for word in path if len(word) >= 3]
                    name = " ".join(path[:-1]) + path[-1]
                    with open("../" + CONFIG.UPLOAD_DIRECTORY + name, "wb") as file:
                        file.write(download_zip.read(file_name))
                    PatreonScrapper.create_map(name)

    def scrape(self):
        while self.url:
            request = requests.get("https://" + self.url, cookies=CONFIG.COOKIES).text
            links = re.findall(CONFIG.LINK_REGEX, request)
            links = [link.replace("amp;", "") for link in links]
            for link in links:
                self.download(link)
            self.url = re.search("\"next\":.*\"https://([^\"]+)\"", request)
            self.url = self.url.group(1) if self.url else None


patreon_scrapper = PatreonScrapper()
patreon_scrapper.scrape()


