"""Here are validators for imagier forms"""


import mimetypes
from django.core.exceptions import ValidationError
from .models import Item


def verify_image_url(value):
    """Checking if url is an image"""
    valid_image_mimetypes = ["image"]
    valid_image_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    mimetype, encoding = mimetypes.guess_type(value)
    if not mimetype:
        if not any(extension in value for extension in valid_image_extensions):
            raise ValidationError('URL non conforme : merci de renseigner un URL vers une image')
    # try:
    #     value.encode('ascii', 'strict')
    # except UnicodeEncodeError:
    #     raise ValidationError('URL non conforme')

def verify_image_not_in_db(value):
    """Verify if the picture url already exists into db"""
    if Item.objects.filter(picture=value).exists():
        raise ValidationError('Cette image existe déjà dans la base de données')
