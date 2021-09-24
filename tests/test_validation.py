import pytest
import random
import string

from config import CONFIG
from errors import ValidationError
from validation import validate_name, validate_extension, validate_dimensions, validate_square_dimensions, validate_tags, validate_battlemap


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


def get_valid_square_dimension():
    return random.choice([str(random.randint(1, 999)), None])


def get_invalid_square_dimension():
    return "".join([random.choice(string.ascii_lowercase) for _ in range(3)])


def test_validate_square_dimensions():
    valid = get_valid_square_dimension()
    invalid = get_invalid_square_dimension()
    assert validate_square_dimensions(valid, valid)
    assert not validate_square_dimensions(invalid, invalid)


def get_valid_tags():
    return ",".join([random.choice(string.ascii_lowercase) for _ in range(CONFIG.MAXIMUM_NAME_LENGTH // 2)])


def get_invalid_tags():
    return "_".join([random.choice(string.ascii_lowercase) for _ in range(CONFIG.MAXIMUM_NAME_LENGTH // 2)])


def test_validate_tags():
    valid = get_valid_tags()
    invalid = get_invalid_tags()
    assert validate_tags(valid)
    assert not validate_tags(invalid)


def test_validate_battlemap():
    valid = {"name": get_valid_name(),
             "extension": get_valid_extension(),
             "width": get_valid_dimension(),
             "height": get_valid_dimension(),
             "tags": get_valid_tags()}

    invalid = {"name": get_invalid_name(),
               "extension": get_invalid_extension(),
               "width": get_invalid_dimension(),
               "height": get_invalid_dimension(),
               "tags": get_invalid_tags()}

    assert validate_battlemap(valid) is None
    with pytest.raises(ValidationError):
        validate_battlemap(invalid)
