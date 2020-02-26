from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    label = models.CharField(max_length=30, unique=False, null=False)
    is_parent = models.BooleanField(default=False, null=False)
    parentcat = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    picture = models.URLField(blank=True, null=False)
    category = models.ManyToManyField(Category, related_name='item', blank=True)

    def __str__(self):
        return self.name

