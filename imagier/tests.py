"""Unit tests about imagier app"""


from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User, Group
from .models import Item, Category
from .forms import ExportImagierForm


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
        self.category = Category.objects.create(
            name=self.cat_name,
            label=self.cat_name,
            is_parent=True
        )
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
        self.subcategory = Category.objects.create(
            name=subcat_name,
            label=subcat_label,
            is_parent=False,
            parentcat=self.category
        )
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
        self.assertEqual(
            response.url,
            "/imagier/subcategory/?category_id={}".format(self.category.id)
        )

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
        self.subcategory = Category.objects.create(
            name=subcat_name,
            label=subcat_label,
            is_parent=False,
            parentcat=self.category
        )
        self.item = Item.objects.create(
            name=item_label,
            picture=item_url,
            label=item_label,
            upper_label=item_label.upper()
        )
        self.item.category.add(self.subcategory)
        self.user = User.objects.create_user('usertest', 'user@test.com', 'testpassword')

    def test_items_view(self):
        """We test 200 returns + template used"""
        self.client.login(username='usertest', password='testpassword')
        url = '{}?{}={}'.format(reverse('imagier:items'), 'subcat_id', self.subcategory.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imagier/items.html')
        self.assertIn(">la vache<", str(response.content))

    def test_items_view_added(self):
        """We test that items is displayed as 'ajouté' if user added it to temp imagier"""
        self.user.item.add(self.item)
        self.client.login(username='usertest', password='testpassword')
        url = '{}?{}={}'.format(reverse('imagier:items'), 'subcat_id', self.subcategory.id)
        response = self.client.get(url)
        self.assertIn(">la vache (ajout\\xc3\\xa9)<", str(response.content))

    def test_item_redirect_if_not_auth(self):
        """We test redirect is no user logged"""
        response = self.client.get(reverse('imagier:items'))
        self.assertEqual(response.status_code, 302)


class ExportPDFViewTestCase(TestCase):
    """we test that we are redirected to render pdf + form is valid"""
    def setUp(self):
        cat_name = "animaux"
        subcat_label = "savane"
        subcat_name = cat_name + "_" + subcat_label
        item_label = "la vache"
        item_url = "https://i.ytimg.com/vi/cQRnf_ycKoE/maxresdefault.jpg"
        self.category = Category.objects.create(name=cat_name, label=cat_name, is_parent=True)
        self.subcategory = Category.objects.create(
            name=subcat_name,
            label=subcat_label,
            is_parent=False,
            parentcat=self.category
        )
        self.item = Item.objects.create(
            name=item_label,
            picture=item_url,
            label=item_label,
            upper_label=item_label.upper()
        )
        self.item.category.add(self.subcategory)
        self.user = User.objects.create_user('usertest', 'user@test.com', 'testpassword')
        self.user.item.add(self.item)

    def test_export_pdf_view(self):
        """We test template used if no form completion"""
        self.client.login(username='usertest', password='testpassword')
        url = '{}?{}={}'.format(reverse('imagier:export_pdf'), 'imagier', 'temp_imagier')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imagier/export_pdf.html')
        self.assertIn("Titre de l&#x27;imagier", str(response.content))

    def test_export_pdf_not_auth(self):
        """We test redirect is no user logged"""
        response = self.client.get(reverse('imagier:export_pdf'))
        self.assertEqual(response.status_code, 302)

    def test_export_pdf_form(self):
        """We test that post form redirect right url"""
        imagier_title = "Mon Imagier"
        file_name = "imagier"
        font_choice = ['mj']
        form = ExportImagierForm({
            'imagier_title': imagier_title,
            'file_name': file_name,
            'font_choice': font_choice,
        })
        self.assertTrue(form.is_valid)
        self.client.login(username='usertest', password='testpassword')
        response = self.client.post(reverse('imagier:export_pdf'), {
            'imagier_title': imagier_title,
            'file_name': file_name,
            'font_choice': font_choice,
        })
        self.assertEqual(response.status_code, 302)
        url = '{}?file_name={}&imagier={}&fontchoice={}'.format(
            reverse('imagier:render_pdf'),
            file_name,
            None,
            font_choice
        )
        self.assertEqual(response.url, url)


class GeneratePDFTestCase(TestCase):
    """We test generate PDF view"""
    def setUp(self):
        cat_name = "animaux"
        subcat_label = "savane"
        subcat_name = cat_name + "_" + subcat_label
        item_label = "la vache"
        item_url = "https://i.ytimg.com/vi/cQRnf_ycKoE/maxresdefault.jpg"
        self.category = Category.objects.create(name=cat_name, label=cat_name, is_parent=True)
        self.subcategory = Category.objects.create(
            name=subcat_name,
            label=subcat_label,
            is_parent=False,
            parentcat=self.category
        )
        self.item = Item.objects.create(
            name=item_label,
            picture=item_url,
            label=item_label,
            upper_label=item_label.upper()
        )
        self.item.category.add(self.subcategory)
        self.user = User.objects.create_user('usertest', 'user@test.com', 'testpassword')
        self.user.item.add(self.item)
        self.file_name = 'imagier'
        self.font_choice = ['mj']

    def test_generatepdf_view_(self):
        """We test that gen pdf return a 200 statut code and use right dic"""
        imagier = 'temp_imagier'
        self.client.login(username='usertest', password='testpassword')
        url = '{}?imagier={}&file_name={}&fontchoice={}'.format(
            reverse('imagier:render_pdf'),
            imagier,
            self.file_name,
            self.font_choice
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # self.assertIn(self.item, response.context['dics'])

    def test_export_pdf_not_auth(self):
        """We test redirect is no user logged"""
        response = self.client.get(reverse('imagier:render_pdf'))
        self.assertEqual(response.status_code, 302)



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
        self.subcategory = Category.objects.create(
            name=subcat_name,
            label=subcat_label,
            is_parent=False,
            parentcat=self.category
        )
        self.item = Item.objects.create(
            name=item_label,
            picture=item_url,
            label=item_label,
            upper_label=item_label.upper()
        )
        self.item.category.add(self.subcategory)
        self.user = User.objects.create_user('usertest', 'user@test.com', 'testpassword')

    def test_add_to_imagier_view(self):
        """We test redirect + item is added to user imagier"""
        self.client.login(username='usertest', password='testpassword')
        url = '{}?{}={}&{}={}'.format(
            reverse('imagier:add_item'),
            'subcat_id',
            self.subcategory.id,
            'item_id',
            self.item.id
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/imagier/items/?subcat_id={}".format(self.subcategory.id))
        self.assertIn(self.item, self.user.item.all())

    def test_delete_from_imagier_view(self):
        """We test redirect + item is removed from user imagier"""
        self.client.login(username='usertest', password='testpassword')
        url = '{}?{}={}&{}={}'.format(
            reverse('imagier:del_item'),
            'subcat_id',
            self.subcategory.id,
            'item_id',
            self.item.id
        )
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


class AddImageToDBProcessTestCase(TestCase):
    """We'll test process to save new pictures into db"""
    def setUp(self):
        cat_name = "animaux"
        subcat_label = "savane"
        subcat_name = cat_name + "_" + subcat_label
        item_label = "la vache"
        item_url = "https://i.ytimg.com/vi/cQRnf_ycKoE/maxresdefault.jpg"
        self.category = Category.objects.create(name=cat_name, label=cat_name, is_parent=True)
        self.subcategory = Category.objects.create(
            name=subcat_name,
            label=subcat_label,
            is_parent=False,
            parentcat=self.category
        )
        self.item = Item.objects.create(
            name=item_label,
            picture=item_url,
            label=item_label,
            upper_label=item_label.upper()
        )
        self.item.category.add(self.subcategory)
        self.user = User.objects.create_user('usertest', 'user@test.com', 'testpassword')
        self.my_group = Group.objects.create(name='école')
        self.my_group.user_set.add(self.user)

    def test_add_image_view(self):
        """we test 200 code and template if user is auth"""
        self.client.login(username='usertest', password='testpassword')
        response = self.client.get(reverse('imagier:add_image'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imagier/add_image.html')

    def test_add_image_post_form(self):
        """We test that user is redirected so save image if form is valid"""
        image_url = 'https://www.anigaido.com/tigre-1-thomas-pierre-xl.jpg'
        cat_choice = self.subcategory
        self.client.login(username='usertest', password='testpassword')
        response = self.client.post(reverse('imagier:add_image'), {
            'item_label': 'le tigre',
            'image_url': image_url,
            'cat_choice': cat_choice.id,
        })
        url = '{}?item_label={}&image_url={}&cat_choice={}'.format(
            reverse('imagier:save_image'),
            'le%20tigre',
            image_url, cat_choice
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, url)

    def test_add_image_redirect_if_not_group(self):
        """We test that user is redirected if he's not in école group"""
        self.my_group.user_set.remove(self.user)
        self.client.login(username='usertest', password='testpassword')
        response = self.client.get(reverse('imagier:add_image'))
        self.assertEqual(response.status_code, 302)


    def test_add_image_redirect_if_not_auth(self):
        """We test redirect is no user logged"""
        response = self.client.get(reverse('imagier:add_image'))
        self.assertEqual(response.status_code, 302)

    def test_save_image_view(self):
        """We test that save image view redirect user and saved image into db"""
        image_url = 'https://www.anigaido.com/tigre-1-thomas-pierre-xl.jpg'
        cat_choice = self.subcategory
        url = '{}?item_label={}&image_url={}&cat_choice={}'.format(
            reverse('imagier:save_image'),
            'le%20tigre',
            image_url,
            cat_choice
        )
        self.client.login(username='usertest', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        url = '{}?item_added=le%20tigre'.format(reverse('imagier:added_successfully'))
        self.assertEqual(response.url, url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imagier/saved_successfully.html')
        self.assertIn(Item.objects.get(name='le tigre'), Item.objects.all())

    def test_save_image_same_label(self):
        """We test that duplicate label increment item name + items is added into inverted cat"""
        image_url = 'https://www.anigaido.com/tigre-1-thomas-pierre-xl.jpg'
        inv_cat = Category.objects.create(
            name='savane_animaux',
            label="animaux",
            is_parent="False",
            parentcat=self.category
        )
        cat_choice = self.subcategory
        url = '{}?item_label={}&image_url={}&cat_choice={}'.format(
            reverse('imagier:save_image'),
            'la%20vache',
            image_url,
            cat_choice
        )
        self.client.login(username='usertest', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(Item.objects.get(name='la vache(1)'), Item.objects.all())
        self.assertIn(Item.objects.get(name='la vache(1)'), inv_cat.item.all())
        self.assertIn(Item.objects.get(name='la vache(1)'), self.subcategory.item.all())

    def test_save_image_redirect_if_not_auth(self):
        """We test redirect is no user logged"""
        response = self.client.get(reverse('imagier:save_image'))
        self.assertEqual(response.status_code, 302)
