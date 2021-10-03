from typing import Dict, Tuple, List

from config import CONFIG


def get_name(data: Dict[str, str]) -> str:
    return data.get("name")


def get_extension(data: Dict[str, str]) -> str:
    return data.get("extension")


def get_hash(data: Dict[str, str]) -> str:
    return data.get("hash")


def get_path(data: Dict[str, str]) -> str:
    directory = CONFIG.UPLOAD_DIRECTORY
    name = get_name(data)
    extension = get_extension(data)
    path = directory + "/" + name + "." + extension
    return path


def get_thumbnail_path(data: Dict[str, str]) -> str:
    directory = CONFIG.THUMBNAIL_DIRECTORY
    name = get_name(data)
    extension = get_extension(data)
    path = directory + "/" + name + "." + extension
    return path


def get_dimensions(data: Dict[str, str]) -> Tuple[str, str]:
    width = data.get("width")
    height = data.get("height")
    return width, height


def get_square_dimensions(data: Dict[str, str]) -> Tuple[str, str]:
    square_width = data.get("square_width")
    square_height = data.get("square_height")
    return square_width, square_height
