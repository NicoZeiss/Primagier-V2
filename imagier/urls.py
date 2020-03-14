from django.conf.urls import url
from . import views


app_name = 'imagier'

urlpatterns = [
    url(r'^category/$', views.category, name="category"),
    url(r'^subcategory/$', views.subcategory, name="subcategory"),
    url(r'^items/$', views.items, name="items"),
    url(r'^add_item/$', views.add_to_imagier, name="add_item"),
    url(r'^delete_item/$', views.del_from_imagier, name="del_item"),
    url(r'^export_pdf/$', views.export_pdf, name="export_pdf"),
    url(r'^pdf/$', views.generate_pdf, name="render_pdf"),
    url(r'^add_image/$', views.add_image, name="add_image"),
    url(r'^save_image/$', views.save_image, name="save_image"),
    url(r'^added_successfully/$', views.added_successfully, name="added_successfully"),
    url(r'^legal_notices/$', views.legal_notices, name="legal_notices"),

]