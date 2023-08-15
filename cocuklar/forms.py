from django.contrib import admin
from .models import  Cocuklar
from dal import autocomplete
from django import forms

class CocuklarAdminForm(forms.ModelForm):
    class Meta:
        model = Cocuklar
        fields = '__all__'
        widgets = {
            'AnneAdi': autocomplete.ModelSelect2(url='kisiler-autocomplete'),
            'BabaAdi': autocomplete.ModelSelect2(url='kisiler-autocomplete'),
        }


