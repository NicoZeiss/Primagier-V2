from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from .models import Category


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
	print(context)

	return render(request, 'imagier/category.html', context)
