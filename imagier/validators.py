from django.core.exceptions import ValidationError
from .models import Item
import mimetypes


def verify_image_url(value):
    VALID_IMAGE_MIMETYPES = ["image"]
    VALID_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]
    mimetype, encoding = mimetypes.guess_type(value)
    if not mimetype:
        if not any(extension in value for extension in VALID_IMAGE_EXTENSIONS):
            raise ValidationError('URL non conforme : merci de renseigner un URL vers une image')

def verify_image_not_in_db(value):
    if Item.objects.filter(picture=value).exists():
        raise ValidationError('Cette image existe déjà dans la base de données')
