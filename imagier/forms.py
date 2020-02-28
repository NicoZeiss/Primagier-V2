from django import forms
from .models import Category


cat_list = []
for item in Category.objects.all():
    if item.is_parent == True:
        cat_list.append(item.label)

class SearchForm(forms.Form):
    # search_widget = forms.TextInput(attrs={'placeholder': 'Aliment...', 'class': 'input-xl'})
    # user_input = forms.CharField(label='', max_length=50, widget=search_widget)
    categorie = forms.CharField()
