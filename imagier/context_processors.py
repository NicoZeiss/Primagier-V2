from .models import Item


def current_imagier(request):
	if request.user.is_authenticated:
		items = request.user.item.all().order_by('imagier_item_user.id')
		return {'current_items': items}
	else:
		return {'current_items': ""}