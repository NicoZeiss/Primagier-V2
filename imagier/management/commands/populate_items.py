from django.core.management.base import BaseCommand, CommandError
from django.core import management
from imagier.models import Category, Item
from imagier.constants import items


class Command(BaseCommand):
    """The command will populate items into db with demo datas"""
    help = "Populate the database with items"

    def handle(self, *args, **options):
        for key in items:
            for item in items[key]:
                cat = Category.objects.get(label=key)
                label_filter = Item.objects.filter(label=item['name'])
                dupl_list = []
                if label_filter:
                    for element in label_filter:
                        dupl_list.append(element)
                    i = len(dupl_list)
                    item_name = '{}({})'.format(item['name'], i)
                    new_item = Item(name=item_name, label=item['name'], upper_label=item['name'].upper(), picture=item['pict'])
                    new_item.save()
                    new_item.category.add(cat)

                else:
                    item_name = item['name']
                    new_item = Item(name=item_name, label=item['name'], upper_label=item['name'].upper(), picture=item['pict'])
                    new_item.save()
                    new_item.category.add(cat)
