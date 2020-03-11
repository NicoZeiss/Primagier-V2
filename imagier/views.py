from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from math import *
from django.views.generic import View
from django.template.loader import get_template
from .models import Category, Item, Favourites
from .utils import render_to_pdf
from .forms import ExportImagierForm, AddImageForm


def is_school_member(user):
    return user.groups.filter(name='école').exists()

def index(request):
	return render(request, 'imagier/index.html')

def category(request):
	if request.user.is_authenticated:
		cat_list = Category.objects.filter(is_parent=True).order_by('label')
		cat_dic = {}
		for item in cat_list:
			cat_dic[item.id] = item.label

		context = {
			'cat_dic': cat_dic
		}

		return render(request, 'imagier/category.html', context)
	else:
		return HttpResponseRedirect(reverse('users:login'))

@login_required
def subcategory(request):
	if 'category_id' in request.GET:
		query = request.GET.get('category_id')
		cat_id = get_object_or_404(Category, id=query)
		category = Category.objects.get(id=query)
		subcat_list = Category.objects.filter(parentcat_id=cat_id).order_by('label')
		subcat_dic = {}
		for item in subcat_list:
			subcat_dic[item.id] = item.label

		context = {
			'subcat_dic': subcat_dic,
			'category_name': category.label
		}

		return render(request, 'imagier/subcategory.html', context)
	else:
		subcat_id = request.GET.get('subcat_id')
		subcat = Category.objects.get(id=subcat_id)
		parcat_id = subcat.parentcat_id
		return HttpResponseRedirect('/imagier/subcategory/?category_id={}'.format(parcat_id))

@login_required
def items(request):
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
	subcat_id = request.GET.get('subcat_id')
	item_id = request.GET.get('item_id')
	_item = Item.objects.get(id=item_id)
	request.user.item.add(_item)
	return HttpResponseRedirect('/imagier/items/?subcat_id={}'.format(subcat_id))

@login_required
def del_from_imagier(request):
	if 'subcat_id' in request.GET:
		subcat_id = request.GET.get('subcat_id')
		item_id = request.GET.get('item_id')
		_item = Item.objects.get(id=item_id)
		request.user.item.remove(_item)
		return HttpResponseRedirect('/imagier/items/?subcat_id={}'.format(subcat_id))
	else:
		item_id = request.GET.get('item_id')
		_item = Item.objects.get(id=item_id)
		request.user.item.remove(_item)
		return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def export_pdf(request):
    imagier = request.GET.get('imagier')
    if request.method == 'POST':
        form = ExportImagierForm(request.POST)
        if form.is_valid():
            imagier_title = form.cleaned_data['imagier_title']
            file_name = form.cleaned_data['file_name']
            font_choice = form.cleaned_data['font_choice']
            return HttpResponseRedirect('{}?file_name={}&imagier={}&fontchoice={}'.format(reverse('imagier:render_pdf'), file_name, imagier, font_choice))
    else:
        form = ExportImagierForm()

    return render(request, 'imagier/export_pdf.html', {'form': form})

@login_required
@user_passes_test(is_school_member)
def add_image(request):
    if request.method == 'POST':
        form = AddImageForm(request.POST)
        if form.is_valid():
            item_label = form.cleaned_data['item_label']
            image_url = form.cleaned_data['image_url']
            cat_choice = form.cleaned_data['cat_choice']
            return HttpResponseRedirect('{}?item_label={}&image_url={}&cat_choice={}'.format(reverse('imagier:save_image'), item_label, image_url, cat_choice))
    else:
        form = AddImageForm()
    return render(request, 'imagier/add_image.html', {'form': form})

@login_required
def added_successfully(request):
    item_name = request.GET.get('item_added')

    context = {
        'item': item_name
    }

    return render(request, 'imagier/saved_successfully.html', context)


class SaveImage(View):
    def get(self, request):
        if request.user.is_authenticated:
            lower_label = request.GET.get('item_label').lower()
            image_url = request.GET.get('image_url')
            cat_choice = request.GET.get('cat_choice')
            cat = Category.objects.get(name=cat_choice)
            upper_label, item_name = self.format_name(lower_label)

            new_item = Item(name=item_name, picture=image_url, label=lower_label, upper_label=upper_label)
            new_item.save()
            new_item.category.add(cat)

            inverted_cat = self.invert_cat_name(cat.name)
            if Category.objects.filter(name=inverted_cat).exists():
                inv_cat = Category.objects.get(name=inverted_cat)
                new_item.category.add(inv_cat)

            return HttpResponseRedirect('{}?item_added={}'.format(reverse('imagier:added_successfully'), lower_label))
        else:
            return HttpResponseRedirect(reverse('users:login'))

    def format_name(self, item_label):
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

    def invert_cat_name(self, cat_name):
        cat = cat_name.replace('_', ' ')
        split_cat = cat.split()
        inverted_cat = split_cat[1] + '_' + split_cat[0]
        return inverted_cat


class GeneratePDF(View):
    def get(self, request):
        if request.user.is_authenticated:
            imagier = request.GET.get('imagier')
            row_file_name = request.GET.get('file_name')
            font_choice = request.GET.get('fontchoice')
            file_name = self.format_file_name(row_file_name)
            items_per_page = 2
            template_name = "imagier/invoice{}.html".format(items_per_page)
            template = get_template(template_name)
            if imagier == 'temp_imagier':
                items = request.user.item.all()
            else:
                favourite = Favourites.objects.get(id=imagier)
                items = favourite.item.all()
            # all_dics = self.create_dics(items_per_page, items)
            all_dics = items

            context = {
                "dics": all_dics,
                "font_choice": font_choice,
            }
            print(context)

            html = template.render(context)
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
        else:
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

    def format_file_name(self, name):
        file_name = name.replace(' ', '_').lower()
        return file_name

