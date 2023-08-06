from django.contrib import admin
from django import forms
from cocuklar.models import Cocuklar
from dal import autocomplete
from django.urls import reverse
from django.utils.html import format_html


# Register your models here.


# Define the customized form for Cocuklar
class CocuklarAdminForm(forms.ModelForm):
    class Meta:
        model = Cocuklar
        fields = '__all__'
        widgets = {
            'AnneAdi': autocomplete.ModelSelect2(url='kisiler-autocomplete'),
            'BabaAdi': autocomplete.ModelSelect2(url='kisiler-autocomplete'),
        }



# Register CocuklarAdmin with the customized form
class CocuklarAdmin(admin.ModelAdmin):
    form = CocuklarAdminForm
    search_fields = ['Adi', 'Soyadi']

    def dosyalar_list(self, obj):
        return ", ".join([str(dosya) for dosya in obj.dosyalar.all()])

    list_display = ['CocukID', 'Adi', 'Soyadi', 'DogumTarihi', 'calculate_age', 'calculate_age1', 'age2', 'Yas16_Tarih',
                'Yas19_Tarih', 'BabaAdi', 'AnneAdi', 'UlkesiID',
                'dosyalar_list']  # Add 'age' or 'calculate_age' to display the age




admin.site.register(Cocuklar, CocuklarAdmin)
