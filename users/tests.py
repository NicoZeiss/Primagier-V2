from django.shortcuts import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .forms import LoginForm, SaveImagierForm, CreateAccountForm
from imagier.models import Item, Category, Favourites


##########################################################################################
#   UNIT TESTS   ##   UNIT TESTS   ##   UNIT TESTS   ##   UNIT TESTS   ##   UNIT TESTS   #
##########################################################################################

class LoginTestCase(TestCase):
    """Testing login page"""

    def setUp(self):
        self.username = "MyUsername"
        self.password = "MyPassword"
        self.email = "MyMail@mail.com"
        self.user = User.objects.create_user(username=self.username, email=self.email)
        self.user.set_password(self.password)
        self.user.save()

    def test_form_login(self):
        """We test that form is valid"""
        form = LoginForm({
            'username': self.username,
            'password': self.password
            })
        self.assertTrue(form.is_valid)

    def test_login_200(self):
        """We test that view returns right template with 200 status"""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imagier/login.html')

    def test_authenticated_login_template(self):
        """We test that authenticated user is redirected if login is successfull"""
        response = self.client.post(reverse('users:login'), {
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(self.user.is_authenticated, True)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_authenticated_wrong_password_template(self):
        """We tes that wrong password does not connect user and raise an error"""
        self.password = "wrong"
        response = self.client.post('/users/login/', {
            'username': self.username,
            'password': self.password
        })
        self.user = authenticate(username=self.username, password=self.password)
        self.login = self.client.login(username=self.username, password=self.password)
        self.assertEqual(self.login, False)
        self.assertIn("Identifiant ou mot de passe incorrect", str(response.content))

    def test_username_error(self):
        """We test that wrong username raise an error"""
        self.username = "wrong"
        response = self.client.post('/users/login/', {
            'username': self.username,
            'password': self.password
        })
        self.user = authenticate(username=self.username, password=self.password)
        self.login = self.client.login(username=self.username, password=self.password)
        self.assertEqual(self.login, False)
        self.assertIn("Identifiant ou mot de passe incorrect", str(response.content))

    def test_login_redirect_index_if_auth(self):
        """Check 302 returns and url"""
        self.user = authenticate(username=self.username, password=self.password)
        self.login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")


class LogoutUserTestCase(TestCase):
    """Testing logout feature"""
    def setUp(self):
        cat_name = "animaux"
        subcat_label = "ferme"
        subcat_name = cat_name + "_" + subcat_label
        item_label = "la vache"
        item_url = "https://i.ytimg.com/vi/cQRnf_ycKoE/maxresdefault.jpg"
        self.category = Category.objects.create(name=cat_name, label=cat_name, is_parent=True)
        self.subcategory = Category.objects.create(name=subcat_name, label=subcat_label, is_parent=False, parentcat=self.category)
        self.item = Item.objects.create(name=item_label, picture=item_url, label=item_label, upper_label=item_label.upper())
        self.item.category.add(self.subcategory)
        self.user = User.objects.create_user('usertest', 'user@test.com', 'testpassword')
        self.user.item.add(self.item)

    def test_logout_user_view(self):
        """wetest that items are deleted from temp imagier if user is going offline"""
        self.user = authenticate(username='usertest', password='testpassword')
        self.login = self.client.login(username='usertest', password='testpassword')
        response = self.client.get(reverse('users:logout'))
        self.assertNotIn(self.item, self.user.item.all())

    def test_redirect_index_when_logout(self):
        """Check 302 returns and url"""
        self.user = authenticate(username='usertest', password='testpassword')
        self.login = self.client.login(username='usertest', password='testpassword')
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_logout_redirect_index_if_not_auth(self):
        """Check 302 returns and url"""
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")


class CreateAccountTestCase(TestCase):
    """Testing create account page"""

    def setUp(self):
        self.newuser = "NewUser"
        self.newpw = "NewPassword"
        self.newemail = "NewEmail@mail.com"
        self.username = "MyUsername"
        self.password = "MyPassword"
        self.email = "MyMail@mail.com"
        self.user = User.objects.create_user(username=self.username, email=self.email)
        self.user.set_password(self.password)
        self.user.save()

    def test_returns_200(self):
        """We test that view returns right template with 200 status"""
        response = self.client.get(reverse('users:create_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imagier/create_account.html')

    def test_redirect_index_if_authenticated(self):
        """We test that user is redirected to index if he's already authenticated"""
        self.user = authenticate(username=self.username, password=self.password)
        self.login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('users:create_account'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_create_account_form(self):
        """We test that form il valid"""
        form = CreateAccountForm({
            'username': self.username,
            'email': self.email,
            'password': self.password
            })
        self.assertTrue(form.is_valid)

    def test_create_account_template_302(self):
        """We test that user is redirected to account if creation is successfull"""
        response = self.client.post('/users/create_account/', {
            'username': self.newuser,
            'email': self.newemail,
            'password': self.newpw
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_short_pw_raise_error(self):
        """We test to short password raise an error"""
        newpw = "Shortpw"
        response = self.client.post('/users/create_account/', {
            'username': self.newuser,
            'email': self.newemail,
            'password': newpw
        })
        error_message = "Le mot de passe doit contenir au moins 8 caract\\xc3\\xa8res"
        self.assertEqual(response.status_code, 200)
        self.assertIn(error_message, str(response.content))

    def test_wrong_email_raise_error(self):
        """We test if error is raised is email is wrong"""
        self.newemail = "test@gmail"
        response = self.client.post('/users/create_account/', {
            'username': self.newuser,
            'email': self.newemail,
            'password': self.newpw
        })
        error_message = "Enter a valid email address."
        self.assertEqual(response.status_code, 200)
        self.assertIn(error_message, str(response.content))

    def test_used_email_raise_error(self):
        """We test if error is raised is email is already used"""
        response = self.client.post('/users/create_account/', {
            'username': self.newuser,
            'email': self.email,
            'password': self.newpw
        })
        error_message = "Cet email est d\\xc3\\xa9j\\xc3\\xa0 utilis\\xc3\\xa9"
        self.assertEqual(response.status_code, 200)
        self.assertIn(error_message, str(response.content))

    def test_used_username_raise_error(self):
        """We test if error is raised is username is already used"""
        response = self.client.post('/users/create_account/', {
            'username': self.username,
            'email': self.email,
            'password': self.newpw
        })
        error_message = "Cet identifiant existe d\\xc3\\xa9j\\xc3\\xa0"
        self.assertEqual(response.status_code, 200)
        self.assertIn(error_message, str(response.content))

##################################################################################
#   INTEGRATION TESTING   ##   INTEGRATION TESTING   ##   INTEGRATION TESTING   #
#################################################################################

class SaveImagierAndFavouritesViewTestCase(TestCase):
    """We test save imagier view"""
    def setUp(self):
        self.imagier_title = "MonImagierTest"
        cat_name = "animaux"
        subcat_label = "ferme"
        subcat_name = cat_name + "_" + subcat_label
        item_label = "la vache"
        item_url = "https://i.ytimg.com/vi/cQRnf_ycKoE/maxresdefault.jpg"
        self.category = Category.objects.create(name=cat_name, label=cat_name, is_parent=True)
        self.subcategory = Category.objects.create(name=subcat_name, label=subcat_label, is_parent=False, parentcat=self.category)
        self.item = Item.objects.create(name=item_label, picture=item_url, label=item_label, upper_label=item_label.upper())
        self.item.category.add(self.subcategory)
        self.user = User.objects.create_user('usertest', 'user@test.com', 'testpassword')
        self.user.item.add(self.item)

    def test_save_imagier_without_post(self):
        """we test template render withour form completion"""
        self.client.login(username='usertest', password='testpassword')
        response = self.client.get(reverse('users:save_imagier'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imagier/save_imagier.html')

    def test_save_imagier_view(self):
        """we test that user is redirected after adding imagier to fav"""
        self.client.login(username='usertest', password='testpassword')
        response = self.client.post('/users/save_imagier/', {
            'imagier_title': self.imagier_title,
        })
        favourite = Favourites.objects.get(user_id=self.user.id)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.imagier_title, favourite.name)
        self.assertEqual(response.url, '{}?favourite_id={}'.format(reverse('users:details'), favourite.id))

    def test_saveimg_redirect_if_not_auth(self):
        """We test redirect is no user logged"""
        response = self.client.get(reverse('users:save_imagier'))
        self.assertEqual(response.status_code, 302)

    def test_favourites_view(self):
        """We test favourites template"""
        favourite = Favourites.objects.create(name=self.imagier_title, user_id=self.user.id)
        add_item = favourite.item.add(self.item)
        self.client.login(username='usertest', password='testpassword')
        response = self.client.get(reverse('users:favourites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imagier/favourites.html')
        self.assertIn("la vache", str(response.content))
        self.assertIn(favourite.name, str(response.content))

    def test_favourites_redirect_if_not_auth(self):
        """We test redirect is no user logged"""
        response = self.client.get(reverse('users:favourites'))
        self.assertEqual(response.status_code, 302)

    def test_delete_favourites_view(self):
        """We test del fav view redirect and fav is deleted from db"""
        favourite = Favourites.objects.create(name=self.imagier_title, user_id=self.user.id)
        add_item = favourite.item.add(self.item)
        self.client.login(username='usertest', password='testpassword')
        url = '{}?{}={}'.format(reverse('users:del_fav'), 'favourite', favourite.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:favourites'))
        self.assertNotIn(favourite, Favourites.objects.filter(user_id=self.user.id))

    def test_del_favourites_redirect_if_not_auth(self):
        """We test redirect is no user logged"""
        response = self.client.get(reverse('users:del_fav'))
        self.assertEqual(response.status_code, 302)


class DetailsViewTestCase(TestCase):
    """We test details view"""
    def setUp(self):
        imagier_title = "MonImagierTest"
        cat_name = "animaux"
        subcat_label = "ferme"
        subcat_name = cat_name + "_" + subcat_label
        item_label = "la vache"
        item_url = "https://i.ytimg.com/vi/cQRnf_ycKoE/maxresdefault.jpg"
        self.category = Category.objects.create(name=cat_name, label=cat_name, is_parent=True)
        self.subcategory = Category.objects.create(name=subcat_name, label=subcat_label, is_parent=False, parentcat=self.category)
        self.item = Item.objects.create(name=item_label, picture=item_url, label=item_label, upper_label=item_label.upper())
        self.item.category.add(self.subcategory)
        self.user = User.objects.create_user('usertest', 'user@test.com', 'testpassword')
        self.favourite = Favourites.objects.create(name=imagier_title, user_id=self.user.id)
        add_item = self.favourite.item.add(self.item)

    def test_details_view(self):
        """We test details template and items in fav"""
        self.client.login(username='usertest', password='testpassword')
        url = '{}?{}={}'.format(reverse('users:details'), 'favourite_id', self.favourite.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imagier/details.html')
        self.assertIn("la vache", str(response.content))
        self.assertIn(self.favourite.name, str(response.content))

    def test_favourites_redirect_if_not_auth(self):
        """We test redirect is no user logged"""
        response = self.client.get(reverse('users:details'))
        self.assertEqual(response.status_code, 302)
