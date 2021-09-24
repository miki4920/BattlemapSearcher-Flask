from config import CONFIG


class ValidationError(Exception):
    def __init__(self):
        self.message = None
        self.error_code = 400


class NameInvalid(ValidationError):
    def __init__(self, name):
        super().__init__()
        self.message = {"error_code": "01",
                        "map_name": name,
                        "invalid": name,
                        "message": f"""Map Name is invalid. It can only contain alphanumerical characters and '_'. 
        Its length must also be within the range:{CONFIG.MINIMUM_NAME_LENGTH},{CONFIG.MAXIMUM_NAME_LENGTH}"""}


class ExtensionInvalid(ValidationError):
    def __init__(self, name, extension):
        super().__init__()
        self.message = {"error_code": "02",
                        "map_name": name,
                        "invalid": extension,
                        "message": f"""Map Extension is invalid. 
        Currently accepted extensions are:{','.join(CONFIG.IMAGE_EXTENSIONS)}"""}


class DimensionsInvalid(ValidationError):
    def __init__(self, name, width, height):
        super().__init__()
        self.message = {"error_code": "03",
                        "map_name": name,
                        "invalid": f"{width},{height}",
                        "message": f"""Map Dimensions are invalid. Currently acceptable minimum dimension is:
        {CONFIG.MINIMUM_IMAGE_DIMENSION}"""}


class SquareDimensionsInvalid(ValidationError):
    def __init__(self, name, square_width, square_height):
        super().__init__()
        self.message = {"error_code": "04",
                        "map_name": name,
                        "invalid": f"{square_width},{square_height}",
                        "message": f"""Map Square Dimensions are invalid. Both dimensions need to either consist of up
                         to 3 digits or be Nones."""}


class ImageInvalid(ValidationError):
    def __init__(self, name, image):
        image_size = len(image)
        super().__init__()
        self.message = {"error_code": "05",
                        "map_name": name,
                        "invalid": image_size,
                        "message": f""":Map Image Size is invalid. Currently accepted size range is:
        {CONFIG.MINIMUM_IMAGE_SIZE_IN_BYTES},{CONFIG.MAXIMUM_IMAGE_SIZE_IN_BYTES}"""}


class HashBlacklisted(ValidationError):
    def __init__(self, name, battlemap_hash):
        super().__init__()
        self.message = {"error_code": "06",
                        "map_name": name,
                        "invalid": battlemap_hash,
                        "message": f"""Map Hash is blacklisted"""}


class HashRepeated(ValidationError):
    def __init__(self, name, battlemap_hash):
        super().__init__()
        self.message = {"error_code": "07",
                        "map_name": name,
                        "invalid": battlemap_hash,
                        "message": f"""Map Hash is already in the database"""}


class TagsInvalid(ValidationError):
    def __init__(self, name, tags):
        super().__init__()
        self.message = {"error_code": "08",
                        "map_name": name,
                        "invalid": tags,
                        "message": f"""Map Tags are invalid."""}
