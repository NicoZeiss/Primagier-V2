from django.conf.urls import url
from . import views


app_name = 'imagier'

urlpatterns = [
    url(r'^category/$', views.category, name="category"),
    url(r'^subcategory/$', views.subcategory, name="subcategory"),
    url(r'îtems/$', views.items, name="items"),
]