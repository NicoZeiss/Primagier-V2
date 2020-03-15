"""Here are functions used into imagier views"""


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Item
from urllib import parse


def render_to_pdf(template_src, context_dict):
    """pisa feature to render pdf"""
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result, encoding='utf-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def format_url(items):
    """Format url to avoid ascii issue"""
    item_list = {}
    for item in items:
        url = item.picture
        scheme, netloc, path, params, query, fragment = parse.urlparse(url)
        new_path = parse.quote(path)
        new_url = parse.urlunparse((scheme, netloc, new_path, params, query, fragment))
        item_list[item.label] = [new_url, item.upper_label]
    return item_list

def format_name(item_label):
    """Format the name if same label already exists into DB"""
    upper_label = item_label.upper()
    labels = Item.objects.filter(label=item_label)
    if labels:
        dupl_list = []
        for label in labels:
            dupl_list.append(label)
            i = len(dupl_list)
            item_name = '{}({})'.format(item_label, i)
    else:
        item_name = item_label
    return upper_label, item_name

def invert_cat_name(cat_name):
    """Check if invert cat exists, to add item into both"""
    cat = cat_name.replace('_', ' ')
    split_cat = cat.split()
    inverted_cat = split_cat[1] + '_' + split_cat[0]
    return inverted_cat

def format_file_name(name):
    """Format the file's name to replace spaces with '_' """
    file_name = name.replace(' ', '_').lower()
    return file_name
