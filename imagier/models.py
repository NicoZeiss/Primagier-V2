"""Here are the 3 models we use into the app"""


from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Category model will contain items with many to many rs"""
    name = models.CharField(max_length=30, unique=True, null=False)
    label = models.CharField(max_length=30, unique=False, null=False)
    is_parent = models.BooleanField(default=False, null=False)
    parentcat = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    """All the items we want to display on pdf"""
    name = models.CharField(max_length=55, unique=True, null=False)
    label = models.CharField(max_length=55, unique=False, null=False)
    upper_label = models.CharField(max_length=55, unique=False, null=False)
    picture = models.URLField(blank=True, null=False, max_length=1000, unique=False)
    category = models.ManyToManyField(Category, related_name='item', blank=True)
    user = models.ManyToManyField(User, related_name='item', blank=True)

    def __str__(self):
        return self.name

    def admin_names(self):
        return ', '.join([a.admin_name for a in self.user.all()])
    admin_names.short_description = "Admin names"

class Favourites(models.Model):
    """Table to save as favourites imagiers"""
    name = models.CharField(max_length=30, unique=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Item, related_name='favourites')

    def __str__(self):
        return self.name
