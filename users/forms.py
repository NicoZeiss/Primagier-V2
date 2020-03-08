from django import forms


class LoginForm(forms.Form):
	required_css_class = 'connect-list-row'
	username = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Identifiant', 'class': 'form-ul', 'id': 'username'}))
	password = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Mot de passe', 'class': 'form-ul', 'type': 'password', 'id': 'password'}))

class SaveImagierForm(forms.Form):
	required_css_class = 'img-form-list-row'
	imagier_title = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Titre de l\'imagier', 'class': 'form-font'}))