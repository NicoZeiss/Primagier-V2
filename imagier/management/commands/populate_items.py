from django.core.management.base import BaseCommand, CommandError
from django.core import management
from imagier.models import Category, Item
from imagier.constants import items


class Command(BaseCommand):
    help = "Populate the database with items"

    def handle(self, *args, **options):
        for key in items:
            for item in items[key]:
                cat = Category.objects.get(label=key)
                new_item = Item(name=item['name'], picture=item['pict'])
                new_item.save()
                new_item.category.add(cat)
