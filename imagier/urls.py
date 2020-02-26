from django.conf.urls import url
from . import views


app_name = 'imagier'

urlpatterns = [
    url(r'^search/$', views.search, name="search"),
]