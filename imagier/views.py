from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from .models import Category, Item
from django.contrib.auth.models import User


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