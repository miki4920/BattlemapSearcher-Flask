import re

from typing import Dict

from config import CONFIG


def validate_name(name: str) -> bool:
    return bool(re.fullmatch(f"[a-z_]{{{CONFIG.MINIMUM_NAME_LENGTH},{CONFIG.MAXIMUM_NAME_LENGTH}}}", name))


def validate_extension(extension: str) -> bool:
    return extension in CONFIG.IMAGE_EXTENSIONS


def validate_dimensions(width: str, height: str) -> bool:
    if not (width.isnumeric() and height.isnumeric()):
        return False
    width, height = int(width), int(height)
    return width > CONFIG.MINIMUM_IMAGE_DIMENSION and height > CONFIG.MINIMUM_IMAGE_DIMENSION


def validate_hash(image):
    pass


def validate_tags(tags):
    pass


def validate_battlemap(battlemap: Dict[str, str]) -> bool:
    name = battlemap.get("name")
    extension = battlemap.get("extension")
    width, height = battlemap.get("width"), battlemap.get("height")
    if not validate_name(name):
        return False
    if not validate_extension(extension):
        return False
    if not validate_dimensions(width, height):
        return False
    return True

