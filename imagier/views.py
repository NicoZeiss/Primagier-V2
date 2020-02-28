from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from .models import Category, Item


def index(request):
	return render(request, 'imagier/index.html')

def category(request):
	cat_list = Category.objects.filter(is_parent=True).order_by('label')
	cat_dic = {}
	for item in cat_list:
		cat_dic[item.id] = item.label

	context = {
		'cat_dic': cat_dic
	}
	return render(request, 'imagier/category.html', context)

def subcategory(request):
	query = request.GET.get('category_id')
	cat_id = get_object_or_404(Category, id=query)
	subcat_list = Category.objects.filter(parentcat_id=cat_id).order_by('label')
	subcat_dic = {}
	for item in subcat_list:
		subcat_dic[item.id] = item.label

	context = {
		'subcat_dic': subcat_dic
	}
	return render(request, 'imagier/subcategory.html', context)

def items(request):
	query = request.GET.get('subcat_id')
	subcat = get_object_or_404(Category, id=query)
	item_list = subcat.item.all()
	item_dic = {}
	for item in item_list:
		item_dic[item.name] = item.picture

	context = {
		'item_dic': item_dic
	}
	return render(request, 'imagier/items.html', context)
