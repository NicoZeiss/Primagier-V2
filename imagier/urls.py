from django.conf.urls import url
from . import views

from . views import GeneratePDF


app_name = 'imagier'

urlpatterns = [
    url(r'^category/$', views.category, name="category"),
    url(r'^subcategory/$', views.subcategory, name="subcategory"),
    url(r'^items/$', views.items, name="items"),
    url(r'^add_item/$', views.add_to_imagier, name="add_item"),
    url(r'^delete_item/$', views.del_from_imagier, name="del_item"),
    url(r'^export_pdf/$', views.export_pdf, name="export_pdf"),
    url(r'^pdf/$', GeneratePDF.as_view(), name="render_pdf"),
]