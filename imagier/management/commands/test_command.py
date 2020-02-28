from django.core.management.base import BaseCommand, CommandError
from django.core import management
from imagier.models import Category


class Command(BaseCommand):
    help = "Populate the database with items"

    def handle(self, *args, **options):
        cat_list = []
        for item in Category.objects.all():
        	if item.is_parent == True:
        		cat_list.append(item.label)
        print(cat_list)

