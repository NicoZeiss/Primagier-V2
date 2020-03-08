from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import Category, Item
from django.contrib.auth.models import User
from math import *
from django.views.generic import View
from django.template.loader import get_template
from .utils import render_to_pdf
from .forms import ImagierForm


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

def subcategory(request):
	if request.user.is_authenticated:
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
	else:
		return HttpResponseRedirect(reverse('users:login'))

def items(request):
	if request.user.is_authenticated:
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
	else:
		return HttpResponseRedirect(reverse('users:login'))

def add_to_imagier(request):
	if request.user.is_authenticated:
		subcat_id = request.GET.get('subcat_id')
		item_id = request.GET.get('item_id')
		_item = Item.objects.get(id=item_id)
		request.user.item.add(_item)

		return HttpResponseRedirect('/imagier/items/?subcat_id={}'.format(subcat_id))
	else:
		return HttpResponseRedirect(reverse('users:login'))

def del_from_imagier(request):
	if request.user.is_authenticated:
		if 'subcat_id' in request.GET:
			subcat_id = request.GET.get('subcat_id')
			item_id = request.GET.get('item_id')
			_item = Item.objects.get(id=item_id)
			request.user.item.remove(_item)
			return HttpResponseRedirect('/imagier/items/?subcat_id={}'.format(subcat_id))

		else:
			item_id = request.GET.get('item_id')
			_item = Item.objects.get(id=item_id)
			print(_item)
			request.user.item.remove(_item)
			return HttpResponseRedirect(request.META['HTTP_REFERER'])
	else:
		return HttpResponseRedirect(reverse('users:login'))

def export_pdf(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ImagierForm(request.POST)
            if form.is_valid():
                imagier_title = form.cleaned_data['imagier_title']
                file_name = form.cleaned_data['file_name']
                return HttpResponseRedirect('{}?file_name={}'.format(reverse('imagier:render_pdf'), file_name))
        else:
            form = ImagierForm()

        return render(request, 'imagier/export_pdf.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('users:login'))

class GeneratePDF(View):
    def get(self, request):
        if request.user.is_authenticated:
            row_file_name = request.GET.get('file_name')
            file_name = self.format_file_name(row_file_name)
            items_per_page = 2
            template_name = "imagier/invoice{}.html".format(items_per_page)
            template = get_template(template_name)
            items = request.user.item.all()
            all_dics = self.create_dics(items_per_page, items)

            context = {
                "dics": all_dics,
            }

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

    def create_dics(self, items_nb, items):
        all_dics = {}
        for i in range(items_nb):
            all_dics['dic{}'.format(i)] = []
        i = 0
        for item in items:
            all_dics['dic{}'.format(i)].append(item)
            i += 1
            if i == items_nb:
                i = 0
        return all_dics

    def format_file_name(self, name):
        file_name = name.replace(' ', '_').lower()
        return file_name
