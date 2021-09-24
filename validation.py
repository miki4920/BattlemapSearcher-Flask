import re
from typing import Dict

from errors import *


def validate_name(name: str) -> bool:
    return bool(re.fullmatch(f"[a-z0-9_]{{{CONFIG.MINIMUM_NAME_LENGTH},{CONFIG.MAXIMUM_NAME_LENGTH}}}", name))


def validate_extension(extension: str) -> bool:
    return extension in CONFIG.IMAGE_EXTENSIONS


def validate_dimensions(width: str, height: str) -> bool:
    if not (width.isnumeric() and height.isnumeric()):
        return False
    width, height = int(width), int(height)
    return width > CONFIG.MINIMUM_IMAGE_DIMENSION and height > CONFIG.MINIMUM_IMAGE_DIMENSION


def validate_square_dimensions(square_width: str, square_height: str) -> bool:
    if type(square_width) == str and type(square_height) == str:
        return bool(re.fullmatch("\d{1,3}", square_width) and re.fullmatch("\d{1,3}", square_height))
    return square_width is None and square_height is None


def validate_tags(tags: str) -> bool:
    return tags is None or bool(re.fullmatch("[a-z,]*", tags))


def validate_battlemap(battlemap: Dict[str, str]) -> None:
    name = battlemap.get("name")
    extension = battlemap.get("extension")
    width, height = battlemap.get("width"), battlemap.get("height")
    square_width, square_height = battlemap.get("square_width"), battlemap.get("square_height")
    tags = battlemap.get("tags")
    if not validate_name(name):
        raise NameInvalid(name)
    if not validate_extension(extension):
        raise ExtensionInvalid(name, extension)
    if not validate_dimensions(width, height):
        raise DimensionsInvalid(name, width, height)
    if not validate_square_dimensions(square_width, square_height):
        raise SquareDimensionsInvalid(name, square_width, square_height)
    if not validate_tags(tags):
        raise TagsInvalid(name, tags)
