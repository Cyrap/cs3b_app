from django.core.files.base import ContentFile
from PIL import Image
import io

MAX_IMAGE_SIZE_MB = 10

def compress_image(image_file):
    """
    Compresses the image to ensure it does not exceed MAX_IMAGE_SIZE_MB.
    """
    img = Image.open(image_file)
    img_format = img.format
    img_io = io.BytesIO()

    img.thumbnail((1024, 1024))
    img.save(img_io, format=img_format, quality=85)

    while img_io.tell() / (1024 * 1024) > MAX_IMAGE_SIZE_MB:
        img_io.seek(0)
        img.save(img_io, format=img_format, quality=75)

    img_io.seek(0)
    return ContentFile(img_io.read(), name=image_file.name)
