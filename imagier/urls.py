from django.conf.urls import url
from . import views


app_name = 'imagier'

urlpatterns = [
    url(r'^category/$', views.category, name="category"),
    url(r'^subcategory/$', views.subcategory, name="subcategory"),
    url(r'items/$', views.items, name="items"),
    url(r'add_item/$', views.add_to_imagier, name="add_item"),
]