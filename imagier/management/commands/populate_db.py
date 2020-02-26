from django.core.management.base import BaseCommand, CommandError
from django.core import management
from imagier.constants import categories, items
from imagier.models import Category, Item


class Command(BaseCommand):
    help = "Populate the database"

    def handle(self, *args, **options):
        # if Category.objects.filter(name='MyCat').exists():
        #     print("yes")
        #     print(Category.objects.filter(name='MyCat'))
  
        # else:
        #     print('ops')
        for key in categories:
            if not Category.objects.filter(name=key).exists():
                parent_cat = Category(name=key, label=key, is_parent=True)
                parent_cat.save()
                print("{} saved :".format(parent_cat.name))
                for value in categories[key]:
                    subcat_name = value + '_' + key
                    if not Category.objects.filter(name=subcat_name).exists():
                        sub_cat = Category(name=subcat_name, label=value, is_parent=False, parentcat=parent_cat)
                        sub_cat.save()
                        print("    {} saved".format(sub_cat.name))
                print("\n")
