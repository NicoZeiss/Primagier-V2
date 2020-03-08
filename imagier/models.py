from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    label = models.CharField(max_length=30, unique=False, null=False)
    is_parent = models.BooleanField(default=False, null=False)
    parentcat = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    label = models.CharField(max_length=30, unique=False, null=False)
    upper_label = models.CharField(max_length=30, unique=False, null=False)
    picture = models.URLField(blank=True, null=False, max_length=1000, unique=True)
    category = models.ManyToManyField(Category, related_name='item', blank=True)
    user = models.ManyToManyField(User, related_name='item', blank=True)

    def __str__(self):
        return self.name

class Favourites(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Item, related_name='item')

    def __str__(self):
        return self.name
