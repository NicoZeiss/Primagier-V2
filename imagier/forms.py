from django import forms
from .validators import verify_image_url, verify_image_not_in_db
from .models import Category, Item


class ExportImagierForm(forms.Form):
    required_css_class = 'img-form-list-row'
    imagier_title = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Titre de l\'imagier', 'class': 'form-font'}))
    file_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Nom du PDF', 'class': 'form-font'}))

class AddImageForm(forms.Form):
    required_css_class = 'img-form-list-row'
    item_label = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Nom de l\'image', 'class': 'form-font'}))
    image_url = forms.URLField(label='', max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'URL de l\'image', 'class': 'form-font'}), validators=[verify_image_url])
    cat_choice = forms.ModelChoiceField(label='', queryset=Category.objects.filter(is_parent=False).order_by('name'))

    def clean(self):
        cleaned_data = super().clean()
        item_url = cleaned_data.get("item_url")
        cat_choice = cleaned_data.get("cat_choice")
        item = Item.objects.get(picture=item_url)
        category = Category.objects.get(name=cat_choice)

        if item.category.filter(category).exists():
            raise forms.ValidationError("BLABLABLA")