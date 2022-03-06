from PIL import Image


from config import CONFIG


Image.MAX_IMAGE_PIXELS = 182750400000


def calculate_image_difference(path):
    resize_width = 9
    resize_height = 8
    image = Image.open(path).convert("LA")
    image = image.resize((resize_width, resize_height), Image.NEAREST)
    pixels = list(image.getdata())
    difference = []
    for row in range(resize_height):
        row_start_index = row * resize_width
        for col in range(resize_width - 1):
            left_pixel_index = row_start_index + col
            difference.append(pixels[left_pixel_index] > pixels[left_pixel_index + 1])
    return difference


def image_hash(path):
    difference = calculate_image_difference(path)
    decimal_value = 0
    hash_string = ""
    for index, value in enumerate(difference):
        if value:
            decimal_value += value * (2 ** (index % 8))
        if index % 8 == 7:
            hash_string += str(
                hex(decimal_value)[2:].rjust(2, "0"))
            decimal_value = 0
    return hash_string


def image_thumbnail(path, thumbnail_path, extension):
    with Image.open(path) as image:
        thumbnail = image.resize((CONFIG.THUMBNAIL_SIZE, CONFIG.THUMBNAIL_SIZE), Image.ANTIALIAS)
        thumbnail.save(thumbnail_path, "JPEG" if extension == "jpg" else extension)


def image_dimensions(path):
    return Image.open(path).size
