from dal import autocomplete
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from cocuklar.models import Cocuklar
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


    # def dosyalar_list(self, obj):
    #     dosyalar_links = []
    #     for dosya in obj.dosyalar.all():
    #         dosya_turu = dosya.DosyaTuru or "N/A"  # Use "N/A" if DosyaTuru is None
    #         dosya_link = f'/admin/dosyalar/dosyalar/{dosya.DosyaID}/change/'
    #         dosya_info = f'DosyaID: {dosya.DosyaID}, DosyaYil: {dosya.DosyaYil}, DosyaNo: {dosya.DosyaNo}, ' \
    #                      f'DosyaTür: {dosya_turu}, Durum: {dosya.DosyaDurumu}, Cocuklar: {dosya.Cocuklar}' \
    #
    #         dosyalar_links.append(format_html('<a href="{}">{}</a>', dosya_link, dosya_info))
    #         return format_html(", ".join(dosyalar_links))
    #
    #
    # dosyalar_list.allow_tags = True
    # dosyalar_list.short_description = 'Dosyalar'


    def dosyalar_list(self, obj):
        return ", ".join([str(dosya) for dosya in obj.dosyalar.all()])


    list_display = ['CocukID', 'Adi', 'Soyadi', 'DogumTarihi', 'calculate_age', 'calculate_age1', 'age2', 'Yas16_Tarih',
                    'Yas19_Tarih', 'BabaAdi', 'AnneAdi', 'UlkesiID','dosyalar_list']  # Add 'age' or 'calculate_age' to display the age

admin.site.register(Cocuklar, CocuklarAdmin)