from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# from PIL import Image
# import requests
# import os
# import io
# from django.core.files.base import ContentFile

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# def downolad_img(item_name, item_url):
#     url = item_url
#     image_file_path = "imagier/downloaded_img/{}".format(item_name)
#     r = requests.get(url)
#     with Image.open(io.BytesIO(r.content)) as im:
#         if im.format == "PNG":
#             extension = "png"
#         elif im.format == "JPEG":
#             extension = "jpeg"
#         elif im.format == "JPG":
#             extension = "jpg"
#         im_file = "{}.{}".format(image_file_path, extension)
#         if os.path.isfile(im_file):
#             pass
#         else:
#             im.save(im_file)