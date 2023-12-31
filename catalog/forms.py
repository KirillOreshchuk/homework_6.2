from django import forms

from catalog.models import Product, Version
from config.settings import BANNED_WORDS


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('owner', 'is_published',)

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        if cleaned_data in BANNED_WORDS:
            raise forms.ValidationError('Продукт запрещен')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        if cleaned_data in BANNED_WORDS:
            raise forms.ValidationError('Продукт запрещен')

        return cleaned_data


class ProductFormModerator(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published',)

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        if cleaned_data in BANNED_WORDS:
            raise forms.ValidationError('Продукт запрещен')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        if cleaned_data in BANNED_WORDS:
            raise forms.ValidationError('Продукт запрещен')

        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = "__all__"
