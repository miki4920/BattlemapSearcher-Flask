import random
import string

from config import CONFIG
from validation import validate_name, validate_extension, validate_dimensions, validate_battlemap


def get_valid_name():
    return "_".join([random.choice(string.ascii_lowercase) for _ in range(CONFIG.MAXIMUM_NAME_LENGTH // 2)])


def get_invalid_name():
    return " ".join([random.choice(string.ascii_lowercase) for _ in range(CONFIG.MAXIMUM_NAME_LENGTH)])


def test_validate_name():
    valid = get_valid_name()
    invalid = get_invalid_name()
    assert validate_name(valid)
    assert not validate_name(invalid)


def get_valid_extension():
    return random.choice(CONFIG.IMAGE_EXTENSIONS)


def get_invalid_extension():
    extension = "".join([random.choice(string.ascii_lowercase) for _ in range(0, 3)])
    while extension in CONFIG.IMAGE_EXTENSIONS:
        extension = "".join([random.choice(string.ascii_lowercase) for _ in range(0, 3)])
    return extension


def test_validate_extension():
    valid = get_valid_extension()
    invalid = get_invalid_extension()
    assert validate_extension(valid)
    assert not validate_extension(invalid)


def get_valid_dimension():
    return str(random.randint(CONFIG.MINIMUM_IMAGE_DIMENSION, CONFIG.MINIMUM_IMAGE_DIMENSION * 10))


def get_invalid_dimension():
    return str(random.randint(0, CONFIG.MINIMUM_IMAGE_DIMENSION - 1))


def test_validate_dimensions():
    valid = get_valid_dimension()
    invalid = get_invalid_dimension()
    assert validate_dimensions(valid, valid)
    assert not validate_dimensions(invalid, invalid)


def test_validate_battlemap():
    valid = {"name": get_valid_name(),
             "extension": get_valid_extension(),
             "width": get_valid_dimension(),
             "height": get_valid_dimension()}

    invalid = {"name": get_invalid_name(),
               "extension": get_invalid_extension(),
               "width": get_invalid_dimension(),
               "height": get_invalid_dimension()}

    assert validate_battlemap(valid)
    assert not validate_battlemap(invalid)
