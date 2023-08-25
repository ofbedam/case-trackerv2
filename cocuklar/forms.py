from django.contrib import admin
from .models import  Cocuk
from dal import autocomplete
from django import forms

class CocuklarAdminForm(forms.ModelForm):
    class Meta:
        model = Cocuk
        fields = '__all__'
        widgets = {
            'AnneAdi': autocomplete.ModelSelect2(url='kisiler-autocomplete'),
            'BabaAdi': autocomplete.ModelSelect2(url='kisiler-autocomplete'),
        }


