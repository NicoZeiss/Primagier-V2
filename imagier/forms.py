"""All the forms we use into imagier app"""


from django import forms
from .validators import verify_image_url
from .models import Category, Item
from .constants import PDF_FONT_CHOICE


class ExportImagierForm(forms.Form):
    """Form to export pdf template"""
    required_css_class = 'img-form-list-row'

    imagier_title = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Titre de l\'imagier', 'class': 'form-font'})
    )

    file_name = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Nom du PDF', 'class': 'form-font'})
    )

    font_choice = forms.MultipleChoiceField(
        label='',
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-font'}),
        choices=PDF_FONT_CHOICE
    )

class AddImageForm(forms.Form):
    """Form to add image template"""
    required_css_class = 'img-form-list-row'

    item_label = forms.CharField(
        label='',
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Nom de l\'image', 'class': 'form-font'})
    )

    image_url = forms.URLField(
        label='',
        max_length=1000,
        widget=forms.TextInput(attrs={'placeholder': 'URL de l\'image', 'class': 'form-font'}),
        validators=[verify_image_url]
    )

    cat_choice = forms.ModelChoiceField(
        label='',
        queryset=Category.objects.filter(is_parent=False).order_by('name'),
        widget=forms.Select(attrs={'class': 'form-font'})
    )

    def clean(self):
        """We check if the url already exists into db only for the same cat"""
        cleaned_data = super().clean()
        item_url = cleaned_data.get("image_url")
        cat_choice = cleaned_data.get("cat_choice")
        items = Item.objects.filter(picture=item_url)
        cat = Category.objects.get(name=cat_choice)
        if any(item in cat.item.all() for item in items):
            raise forms.ValidationError("Cette image existe déjà dans la base de données")
