from config import CONFIG


class ValidationError(Exception):
    pass


class NameInvalid(ValidationError):
    def __init__(self, name):
        self.message = f"""01:Map Name is invalid. It can only contain alphanumerical characters and '_'. 
        Its length must also be within this range:{CONFIG.MINIMUM_NAME_LENGTH},{CONFIG.MAXIMUM_NAME_LENGTH}:{name}"""


class ExtensionInvalid(ValidationError):
    def __init__(self, extension):
        self.message = f"""02:Map Extension is invalid. 
        Currently accepted extensions are:{','.join(CONFIG.IMAGE_EXTENSIONS)}):{extension}"""


class DimensionsInvalid(ValidationError):
    def __init__(self, width, height):
        self.message = f"""03:Map Dimensions are invalid. Currently acceptable minimum dimension is:
        {CONFIG.MINIMUM_IMAGE_DIMENSION}:{width},{height}"""


class ImageInvalid(ValidationError):
    def __init__(self, image):
        image_size = len(image)
        self.message = f"""03:Map Image is invalid. Currently accepted size range is:
        {CONFIG.MINIMUM_IMAGE_SIZE_IN_BYTES},{CONFIG.MAXIMUM_IMAGE_SIZE_IN_BYTES}:{image_size}"""


class HashBlacklisted(ValidationError):
    def __init__(self, name, battlemap_hash):
        self.message = f"04:Map Hash is blacklisted:{name}:{battlemap_hash}"


class HashRepeated(ValidationError):
    def __init__(self, name, battlemap_hash):
        self.message = f"05:Map Hash is already in the database:{name}:{battlemap_hash}"


class SquareDimensionsNotAccepted(ValidationError):
    def __init__(self, square_width, square_height):
        self.message = f"07:Map Picture is missing one of the square dimensions:{square_width},{square_height}"


class SquareDimensionsNotInRange(ValidationError):
    def __init__(self, square_width, square_height):
        self.message = f"08:One of the square dimensions is not an Integer or Null:{square_width},{square_height}"


class UploaderNotAlphanumerical(ValidationError):
    def __init__(self, uploader):
        self.message = f"09:Map Uploader contains non-alphanumerical characters:{uploader}"


class UploaderNotInRange(ValidationError):
    def __init__(self, uploader):
        self.message = f"10:Map Uploader has wrong length:{uploader}"


class TagsNotAccepted(ValidationError):
    def __init__(self, tags):
        self.message = f"11:Map Tags are in a wrong format:{tags}"