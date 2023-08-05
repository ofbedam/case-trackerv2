# dosyayon/forms.py
from django.contrib import admin
from .models import Dosyalar, Cocuklar, Kisiler
from dal import autocomplete
from django import forms

class DosyalarAdminForm(forms.ModelForm):
    class Meta:
        model = Dosyalar
        fields = '__all__'
        widgets = {
            'CocukID': autocomplete.ModelSelect2Multiple(
                url='cocuklar-autocomplete',  # Replace this with the URL pattern for CocuklarAutocomplete view
            )
        }

    basvurucu = forms.ModelChoiceField(queryset=Kisiler.objects.all(), label='Başvurucu', widget=autocomplete.ModelSelect2(url='kisiler-autocomplete'))
    karsi_taraf = forms.ModelChoiceField(queryset=Kisiler.objects.all(), label='Karşı Taraf', widget=autocomplete.ModelSelect2(url='kisiler-autocomplete'))




class DosyalarAdmin(admin.ModelAdmin):
    form = DosyalarAdminForm

admin.site.register(Dosyalar, DosyalarAdmin)


class CocuklarAdminForm(forms.ModelForm):
    class Meta:
        model = Cocuklar
        fields = '__all__'
        widgets = {
            'AnneAdi': autocomplete.ModelSelect2(url='kisiler-autocomplete'),
            'BabaAdi': autocomplete.ModelSelect2(url='kisiler-autocomplete'),
        }