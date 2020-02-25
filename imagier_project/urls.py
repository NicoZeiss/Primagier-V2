from django.contrib import admin
from django.urls import path, include
from imagier import views


urlpatterns = [
    path('site_admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('imagier/', include('imagier.urls', namespace='imagier')),
]
