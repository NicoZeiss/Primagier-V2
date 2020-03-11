from django.conf.urls import url
from . import views


app_name = 'users'

urlpatterns = [
    url(r'^login/$', views.user_login, name="login"),
    url(r'^logout/$', views.user_logout, name="logout"),
    url(r'^save_imagier/$', views.save_imagier, name='save_imagier'),
    url(r'^favourites/$', views.favourites, name='favourites'),
    url(r'^details/$', views.details, name='details'),
    url(r'^del_fav/$', views.del_favourite, name='del_fav'),
]