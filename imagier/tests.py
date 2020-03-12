from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .models import Item, Category, Favourites


##########################################################################################
#   UNIT TESTS   ##   UNIT TESTS   ##   UNIT TESTS   ##   UNIT TESTS   ##   UNIT TESTS   #
##########################################################################################

class IndexViewTestCase(TestCase):
    """Testing index page"""

    def test_index_view(self):
        """We test 200 returns + template used"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imagier/index.html')


class CategoryViewTestCase(TestCase):
	"""We test category view + template"""

	def setUp(self):
		self.cat_name = "animaux"
		self.category = Category.objects.create(name=self.cat_name, label=self.cat_name, is_parent=True)
		self.user = User.objects.create_user('usertest', 'user@test.com', 'testpassword')

	def test_category_view(self):
		"""We test 200 returns + template used"""
		self.client.login(username='usertest', password='testpassword')
		response = self.client.get(reverse('imagier:category'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'imagier/category.html')
		self.assertIn(self.cat_name, str(response.content))

	def test_category_redirect_if_not_auth(self):
		"""We test redirect to login template is no user logged"""
		response = self.client.get(reverse('imagier:category'))
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, "/users/login/")


class SubcategoryViewTestCase(TestCase):
	"""We test subcategory view + template"""

	def setUp(self):
		cat_name = "animaux"
		subcat_label = "savane"
		subcat_name = cat_name + "_" + subcat_label
		self.category = Category.objects.create(name=cat_name, label=cat_name, is_parent=True)
		self.subcategory = Category.objects.create(name=subcat_name, label=subcat_label, is_parent=False, parentcat=self.category)
		self.user = User.objects.create_user('usertest', 'user@test.com', 'testpassword')

	def test_subcategory_view(self):
		"""We test 200 returns + template used"""
		self.client.login(username='usertest', password='testpassword')
		url = '{}?{}={}'.format(reverse('imagier:subcategory'), 'category_id', self.category.id)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'imagier/subcategory.html')
		self.assertIn("savane", str(response.content))

	def test_subcategory_view_from_item(self):
		"""We test 200 returns + template used when we access to sub from item view"""
		self.client.login(username='usertest', password='testpassword')
		url = '{}?{}={}'.format(reverse('imagier:subcategory'), 'subcat_id', self.subcategory.id)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, "/imagier/subcategory/?category_id={}".format(self.category.id))

	def test_subcategory_redirect_if_not_auth(self):
		"""We test redirect is no user logged"""
		response = self.client.get(reverse('imagier:subcategory'))
		self.assertEqual(response.status_code, 302)


class ItemsViewTestCase(TestCase):
	"""We test items view + template"""

	def setUp(self):
		cat_name = "animaux"
		subcat_label = "savane"
		subcat_name = cat_name + "_" + subcat_label
		item_label = "la vache"
		item_url = "https://i.ytimg.com/vi/cQRnf_ycKoE/maxresdefault.jpg"
		self.category = Category.objects.create(name=cat_name, label=cat_name, is_parent=True)
		self.subcategory = Category.objects.create(name=subcat_name, label=subcat_label, is_parent=False, parentcat=self.category)
		self.item = Item.objects.create(name=item_label, picture=item_url, label=item_label, upper_label=item_label.upper())
		self.item.category.add(self.subcategory)
		self.user = User.objects.create_user('usertest', 'user@test.com', 'testpassword')

	def test_items_view(self):
		"""We test 200 returns + template used"""
		self.client.login(username='usertest', password='testpassword')
		url = '{}?{}={}'.format(reverse('imagier:items'), 'subcat_id', self.subcategory.id)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'imagier/items.html')
		self.assertIn("la vache", str(response.content))

	def test_item_redirect_if_not_auth(self):
		"""We test redirect is no user logged"""
		response = self.client.get(reverse('imagier:subcategory'))
		self.assertEqual(response.status_code, 302)


class ExportPDFViewTestCase(TestCase):
	"""we test that we are redirected to render pdf + form is valid"""
	pass


##################################################################################
#   INTEGRATION TESTING   ##   INTEGRATION TESTING   ##   INTEGRATION TESTING   #
#################################################################################

class AddDeleteItemFromImagierViewTestCase(TestCase):
	"""We test view to add pictures to imagier and view to delete it"""

	def setUp(self):
		cat_name = "animaux"
		subcat_label = "savane"
		subcat_name = cat_name + "_" + subcat_label
		item_label = "la vache"
		item_url = "https://i.ytimg.com/vi/cQRnf_ycKoE/maxresdefault.jpg"
		self.category = Category.objects.create(name=cat_name, label=cat_name, is_parent=True)
		self.subcategory = Category.objects.create(name=subcat_name, label=subcat_label, is_parent=False, parentcat=self.category)
		self.item = Item.objects.create(name=item_label, picture=item_url, label=item_label, upper_label=item_label.upper())
		self.item.category.add(self.subcategory)
		self.user = User.objects.create_user('usertest', 'user@test.com', 'testpassword')

	def test_add_to_imagier_view(self):
		"""We test redirect + item is added to user imagier"""
		self.client.login(username='usertest', password='testpassword')
		url = '{}?{}={}&{}={}'.format(reverse('imagier:add_item'), 'subcat_id', self.subcategory.id, 'item_id', self.item.id)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, "/imagier/items/?subcat_id={}".format(self.subcategory.id))
		self.assertIn(self.item, self.user.item.all())

	def test_delete_from_imagier_view(self):
		"""We test redirect + item is removed from user imagier"""
		self.client.login(username='usertest', password='testpassword')
		url = '{}?{}={}&{}={}'.format(reverse('imagier:del_item'), 'subcat_id', self.subcategory.id, 'item_id', self.item.id)
		response = self.client.get(url)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, "/imagier/items/?subcat_id={}".format(self.subcategory.id))
		self.assertNotIn(self.item, self.user.item.all())

	def test_add_item_redirect_if_not_auth(self):
		"""We test redirect is no user logged"""
		response = self.client.get(reverse('imagier:add_item'))
		self.assertEqual(response.status_code, 302)

	def test_delete_item_redirect_if_not_auth(self):
		"""We test redirect is no user logged"""
		response = self.client.get(reverse('imagier:del_item'))
		self.assertEqual(response.status_code, 302)
