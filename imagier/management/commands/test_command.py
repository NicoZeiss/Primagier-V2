from django.core.management.base import BaseCommand, CommandError
from django.core import management
from imagier.models import Category
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Populate the database with items"

    def handle(self, *args, **options):
    	username = "devaccount"
    	email = "dev@gmail.com"
    	password = "12345678"
    	user = User.objects.create_user(username, email, password)
    	user.save()

