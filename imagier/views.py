from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect


def index(request):
	return render(request, 'imagier/index.html')

def search(request):
	return render(request, 'imagier/search.html')
