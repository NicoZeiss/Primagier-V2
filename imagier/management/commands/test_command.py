from django.core.management.base import BaseCommand, CommandError
from django.core import management
from imagier.models import Category, Item
from django.contrib.auth.models import User
from PIL import Image
import os.path
import requests
import io
from django.core.files.base import ContentFile
import mimetypes


class Command(BaseCommand):
    help = "Populate the database with items"


    def handle(self, *args, **options):
        url = "https://i.ytimg.com/vi/cQRnf_ycKoE/maxresdefault.jpg"
        lower_label = "la vache"
        mycat = "animaux_marins"
        upper_label, item_name = self.format_name(lower_label)
        inv_cat = self.invert_cat_name(mycat)
        cat = Category.objects.get(name=mycat)

        new_item = Item(name=item_name, picture=url, label=lower_label, upper_label=upper_label)
        new_item.save()
        new_item.category.add(cat)

        if Category.objects.filter(name=inv_cat).exists():
            inverted_cat = Category.objects.get(name=inv_cat)
            new_item.category.add(inverted_cat)            

    def invert_cat_name(self, cat_name):
        cat = cat_name.replace('_', ' ')
        split_cat = cat.split()
        inverted_cat = split_cat[1] + '_' + split_cat[0]
        return inverted_cat

    def format_name(self, item_label):
        upper_label = item_label.upper()
        labels = Item.objects.filter(label=item_label)
        if labels:
            dupl_list = []
            for label in labels:
                dupl_list.append(label)
                i = len(dupl_list)
                item_name = '{}({})'.format(item_label, i)
        else:
            item_name = item_label
        return upper_label, item_name
