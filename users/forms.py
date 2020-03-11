from django import forms
from .validators import unique_id, unique_email, password_min_length


class LoginForm(forms.Form):
	required_css_class = 'connect-list-row'
	username = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Identifiant', 'class': 'form-ul', 'id': 'username'}))
	password = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Mot de passe', 'class': 'form-ul', 'type': 'password', 'id': 'password'}))

class SaveImagierForm(forms.Form):
	required_css_class = 'img-form-list-row'
	imagier_title = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Titre de l\'imagier', 'class': 'form-font'}))

class CreateAccountForm(forms.Form):
	required_css_class = 'connect-list-row'
	username = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Identifiant', 'class': 'form-ul'}), validators=[unique_id])
	email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-ul'}), validators=[unique_email])
	password = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Mot de passe', 'class': 'form-ul', 'type': 'password'}), validators=[password_min_length])