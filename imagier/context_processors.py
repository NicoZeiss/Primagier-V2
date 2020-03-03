from .models import Item


def current_imagier(request):
	if request.user.is_authenticated:
		items = request.user.item.all()
		return {'current_items': items}
	else:
		return {'current_items': ""}