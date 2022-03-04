from PIL import Image
from io import BytesIO


def calculate_image_difference(image):
    resize_width = 9
    resize_height = 8
    image = Image.open(BytesIO(image)).convert("LA")
    image = image.resize((resize_width, resize_height), Image.NEAREST)
    pixels = list(image.getdata())
    difference = []
    for row in range(resize_height):
        row_start_index = row * resize_width
        for col in range(resize_width - 1):
            left_pixel_index = row_start_index + col
            difference.append(pixels[left_pixel_index] > pixels[left_pixel_index + 1])
    return difference


def hash_image(image):
    difference = calculate_image_difference(image)
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
