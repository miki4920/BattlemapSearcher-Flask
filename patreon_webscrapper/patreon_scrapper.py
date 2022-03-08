import re
from io import BytesIO
from zipfile import ZipFile

import requests

from config import CONFIG
from image import image_hash, image_thumbnail, image_dimensions
from model import Map, Tag, db, create_map


class PatreonScrapper(object):
    def __init__(self):
        self.url = CONFIG.STARTING_URL

    @staticmethod
    def get_name(name):
        if re.match("[A-Z0-9][A-Z0-9]", name[-2:]):
            return name[:-2]
        return name

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
                    path = " ".join(path[:-1]) + path[-1]
                    name, extension = path[:-4], path[-3:]
                    name = PatreonScrapper.get_name(name)
                    battlemap_hash = image_hash(BytesIO(download_zip.read(file_name)))
                    if Map.query.filter_by(hash=battlemap_hash).first() is None and Map.query.filter_by(
                            path=CONFIG.UPLOAD_DIRECTORY + path).first() is None:
                        with open("../" + CONFIG.UPLOAD_DIRECTORY + path, "wb") as file:
                            file.write(download_zip.read(file_name))
                        image_thumbnail("../" + CONFIG.UPLOAD_DIRECTORY + path,
                                        "../" + CONFIG.THUMBNAIL_DIRECTORY + path, extension)
                        width, height = image_dimensions("../" + CONFIG.UPLOAD_DIRECTORY + path)
                        square_width, square_height = width // 140, height // 140
                        create_map(name=name, extension=extension, path=path, width=width, height=height,
                                   square_width=square_width,
                                   square_height=square_height, hash=battlemap_hash)

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
