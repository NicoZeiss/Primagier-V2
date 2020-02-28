from django.conf.urls import url
from . import views


app_name = 'imagier'

urlpatterns = [
    url(r'^category/$', views.category, name="category"),
]