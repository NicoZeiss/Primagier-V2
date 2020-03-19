"""Here are alls the views from imagier app"""

import os
from imagier_project.settings import BASE_DIR
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Category, Item, Favourites
from .utils import render_to_pdf, format_name, invert_cat_name, format_file_name, format_url
from .forms import ExportImagierForm, AddImageForm


def is_school_member(user):
    """Filter user by group école"""
    return user.groups.filter(name='école').exists()

def index(request):
    """Render index template"""
    return render(request, 'imagier/index.html')

def legal_notices(request):
    """Render legal notices template"""
    return render(request, 'imagier/legal_notices.html')

def category(request):
    """Display all parent cat"""
    if request.user.is_authenticated:
        cat_list = Category.objects.filter(is_parent=True).order_by('label')
        cat_dic = {}
        for item in cat_list:
            cat_dic[item.id] = item.label

        context = {
            'cat_dic': cat_dic
        }

        return render(request, 'imagier/category.html', context)
    return HttpResponseRedirect(reverse('users:login'))

@login_required
def subcategory(request):
    """Display all subcat from parent cat choice"""
    if 'category_id' in request.GET:
        query = request.GET.get('category_id')
        cat_id = get_object_or_404(Category, id=query)
        parent_cat = Category.objects.get(id=query)
        subcat_list = Category.objects.filter(parentcat_id=cat_id).order_by('label')
        subcat_dic = {}
        for item in subcat_list:
            subcat_dic[item.id] = item.label

        context = {
            'subcat_dic': subcat_dic,
            'category_name': parent_cat.label
        }

        return render(request, 'imagier/subcategory.html', context)

    subcat_id = request.GET.get('subcat_id')
    subcat = Category.objects.get(id=subcat_id)
    parcat_id = subcat.parentcat_id
    return HttpResponseRedirect('/imagier/subcategory/?category_id={}'.format(parcat_id))

@login_required
def items(request):
    """Display all items from a subcat choice"""
    query = request.GET.get('subcat_id')
    subcat = get_object_or_404(Category, id=query)
    item_list = subcat.item.all()
    item_dic = {}
    for item in item_list:
        if len(item.user.filter(username=request.user.username)) != 0:
            item_dic[item] = True
        else:
            item_dic[item] = False

    context = {
        'item_dic': item_dic,
        'subcat': subcat,
    }

    return render(request, 'imagier/items.html', context)

@login_required
def add_to_imagier(request):
    """Add an item to temp imagier"""
    subcat_id = request.GET.get('subcat_id')
    item_id = request.GET.get('item_id')
    _item = Item.objects.get(id=item_id)
    request.user.item.add(_item)
    return HttpResponseRedirect('/imagier/items/?subcat_id={}'.format(subcat_id))

@login_required
def del_from_imagier(request):
    """Delete an item from temp imagier"""
    if 'subcat_id' in request.GET:
        subcat_id = request.GET.get('subcat_id')
        item_id = request.GET.get('item_id')
        _item = Item.objects.get(id=item_id)
        request.user.item.remove(_item)
        return HttpResponseRedirect('/imagier/items/?subcat_id={}'.format(subcat_id))

    item_id = request.GET.get('item_id')
    _item = Item.objects.get(id=item_id)
    request.user.item.remove(_item)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def del_tempimg(request):
    request.user.item.clear()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def export_pdf(request):
    """Display template to chose pdf name + fonts to use"""
    imagier = request.GET.get('imagier')
    if request.method == 'POST':
        form = ExportImagierForm(request.POST)
        if form.is_valid():
            # imagier_title = form.cleaned_data['imagier_title']
            file_name = form.cleaned_data['file_name']
            font_choice = form.cleaned_data['font_choice']
            return HttpResponseRedirect('{}?file_name={}&imagier={}&fontchoice={}'.format(
                reverse('imagier:render_pdf'),
                file_name, imagier,
                font_choice
            ))
    else:
        form = ExportImagierForm()

    return render(request, 'imagier/export_pdf.html', {'form': form})

# Only users from école group can add images to DB
@login_required
@user_passes_test(is_school_member)
def add_image(request):
    """Display form to add new image to DB"""
    if request.method == 'POST':
        form = AddImageForm(request.POST)
        if form.is_valid():
            item_label = form.cleaned_data['item_label']
            image_url = form.cleaned_data['image_url']
            cat_choice = form.cleaned_data['cat_choice']
            return HttpResponseRedirect('{}?item_label={}&image_url={}&cat_choice={}'.format(
                reverse('imagier:save_image'),
                item_label,
                image_url,
                cat_choice
            ))
    else:
        form = AddImageForm()
    return render(request, 'imagier/add_image.html', {'form': form})

@login_required
def added_successfully(request):
    """Confirm that item is rightly added to DB"""
    item_name = request.GET.get('item_added')

    context = {
        'item': item_name
    }

    return render(request, 'imagier/saved_successfully.html', context)

def save_image(request):
    """Save image into the DB, from add image template"""
    if request.user.is_authenticated:
        lower_label = request.GET.get('item_label').lower()
        image_url = request.GET.get('image_url')
        cat_choice = request.GET.get('cat_choice')
        cat = Category.objects.get(name=cat_choice)
        upper_label, item_name = format_name(lower_label)

        new_item = Item(
            name=item_name,
            picture=image_url,
            label=lower_label,
            upper_label=upper_label
        )
        new_item.save()
        new_item.category.add(cat)

        inverted_cat = invert_cat_name(cat.name)
        if Category.objects.filter(name=inverted_cat).exists():
            inv_cat = Category.objects.get(name=inverted_cat)
            new_item.category.add(inv_cat)

        return HttpResponseRedirect('{}?item_added={}'.format(
            reverse('imagier:added_successfully'),
            lower_label
        ))
    return HttpResponseRedirect(reverse('users:login'))

def generate_pdf(request):
    """Generate the PDF from export pdf template"""
    if request.user.is_authenticated:
        imagier = request.GET.get('imagier')
        file_name = format_file_name(request.GET.get('file_name'))
        font_choice = request.GET.get('fontchoice')
        # Items user want to display per page | 2 for V1
        items_per_page = 2
        template_name = "imagier/invoice{}.html".format(items_per_page)
        # check if export is from temp imagier or favourites
        if imagier == 'temp_imagier':
            item_list = request.user.item.all().order_by('imagier_item_user.id')
        else:
            favourite = Favourites.objects.get(id=imagier)
            item_list = favourite.item.all().order_by('imagier_favourites_item.id')
        # all_dics = self.create_dics(items_per_page, items)
        fonts_url = file_path = os.path.join(BASE_DIR, 'imagier/static/imagier/fonts/')

        formated_items = format_url(item_list)

        context = {
            "dics": formated_items,
            "font_choice": font_choice,
            "fonts_url": fonts_url,
        }

        # PDF rendering
        pdf = render_to_pdf(template_name, context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "%s.pdf" %(file_name)
            content = "inline; filename=%s" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
    return HttpResponseRedirect(reverse('users:login'))

# def create_dics(self, items_nb, items):
#     all_dics = {}
#     for i in range(items_nb):
#         all_dics['dic{}'.format(i)] = []
#     i = 0
#     for item in items:
#         all_dics['dic{}'.format(i)].append(item)
#         i += 1
#         if i == items_nb:
#             i = 0
#     return all_dics
