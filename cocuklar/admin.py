from django.contrib import admin
from django import forms
from cocuklar.models import Cocuklar
from dal import autocomplete
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

    list_display = ['Adi', 'Soyadi', 'dosyalar_list']

admin.site.register(Cocuklar, CocuklarAdmin)
