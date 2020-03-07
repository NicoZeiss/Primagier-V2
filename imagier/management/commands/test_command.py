from django.core.management.base import BaseCommand, CommandError
from django.core import management
from imagier.models import Category, Item
from django.contrib.auth.models import User
from PIL import Image
import os.path
import requests
import io
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = "Populate the database with items"

    def handle(self, *args, **options):
    	url = "https://vignette.wikia.nocookie.net/jurassicpark/images/7/73/Blue_Fallen_Kingdom.png/revision/latest?cb=20181014190546&path-prefix=fr"
    	image_file_path = "imagier/downloaded_img/image"
    	item = Item.objects.get(id=105)
    	r = requests.get(url)
    	with Image.open(io.BytesIO(r.content)) as im:
    		if im.format == "PNG":
    			extension = "png"
    		elif im.format == "JPEG":
    			extension = "jpeg"
    		elif im.format == "JPG":
    			extension = "jpg"
    		im_file = "{}.{}".format(image_file_path, extension)
    		if os.path.isfile(im_file):
    			print("already exists")
    		else:
    			im.save(im_file)