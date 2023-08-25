 # cocuklar/admin.py

from dal import autocomplete
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from cocuklar.models import Cocuk
from Dosya.models import Dosya
from dosya2.dosyaiade.models import DosyaCKIade
from dosya2.dosyailiski.models import DosyaCKIliski
# Register your models here.


from django.urls import reverse
# Define the customized form for Cocuklar
class CocuklarAdminForm(forms.ModelForm):
    class Meta:
        model = Cocuk
        fields = '__all__'
        widgets = {
            'AnneAdi': autocomplete.ModelSelect2(url='kisiler-autocomplete'),
            'BabaAdi': autocomplete.ModelSelect2(url='kisiler-autocomplete'),
            'Ulkesi' : autocomplete.ModelSelect2(url='CountryAutocomplete'),
        }


# Register CocuklarAdmin with the customized form
class CocuklarAdmin(admin.ModelAdmin):
    form = CocuklarAdminForm
    search_fields = ['Adi', 'IkinciAdi', 'Soyadi']



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


    # def dosyalar_list(self, obj):
    #     return ", ".join([str(dosya) for dosya in obj.dosyalar.all()])

    # def dosya_list(self, obj):
    #     dosya_infos = []
    #
    #     for dosya in obj.dosya.all():
    #         dosya_kodu = dosya.dosya_kodu if dosya.dosya_kodu else "Bilinmiyor"
    #         dosya_kodu_adi = dict(Dosya.DOSYA_KODLARI).get(dosya_kodu, "Bilinmiyor")
    #         yil = dosya.yil if dosya.yil else "Bilinmiyor"
    #         sayi = dosya.sayi if dosya.sayi else "Bilinmiyor"
    #
    #         dosya_info = [
    #             f"{dosya_kodu}",
    #             f"{dosya_kodu_adi}",
    #             f"{yil}",
    #             f"/{sayi}",
    #         ]
    #         dosya_infos.append(dosya_info)
    #
    #     if not dosya_infos:
    #         return "Dosya bilgisi bulunmuyor"
    #
    #     formatted_dosya_infos = "\n\n&\n".join(["\n".join(info) for info in dosya_infos])
    #     return formatted_dosya_infos

    def dosya_list(self, obj):
        dosya_infos = []

        for dosya in obj.dosya.all():
            dosya_kodu = dosya.dosya_kodu if dosya.dosya_kodu else "Bilinmiyor"
            dosya_kodu_adi = dict(Dosya.DOSYA_KODLARI).get(dosya_kodu, "Bilinmiyor")
            yil = dosya.yil if dosya.yil else "Bilinmiyor"
            sayi = dosya.sayi if dosya.sayi else "Bilinmiyor"

            # dosya_url = reverse("admin:dosya_duzenle",
            #                     args=[dosya.id])  # 'dosya_duzenle' burada dosya düzenleme URL adınız olsun
            # dosya_link = f'<a href="{dosya_url}">Dosyayı Düzenle</a>'

            dosya_info = [
                f"Dosya Kodu: {dosya_kodu}",
                f"Dosya Adı: {dosya_kodu_adi}",
                f"Yıl: {yil}",
                f"Sayı: {sayi}",
            ]
            dosya_infos.append(dosya_info)

        if not dosya_infos:
            return "Dosya bilgisi bulunmuyor"

        formatted_dosya_infos = "\n\n".join(["\n".join(info) for info in dosya_infos])
        return formatted_dosya_infos
        if not dosya_infos:
            return "Dosya bilgisi bulunmuyor2"

        formatted_dosya_infos = "<br><br>".join(["<br>".join(info) for info in dosya_infos])
        return format_html(formatted_dosya_infos)

    def dosya2_iade_list(self, obj):
        dosya2_iade_infos = []

        for cocuk_dosya2iade in obj.cocuk_dosya2iade.all():
            yil = cocuk_dosya2iade.yil if cocuk_dosya2iade.yil else "Bilinmiyor"
            sayi = cocuk_dosya2iade.sayi if cocuk_dosya2iade.sayi else "Bilinmiyor"
            id = cocuk_dosya2iade.id if cocuk_dosya2iade.id else "Bilinmiyor"

            dosya2_iade_info = [
                f"id: {id}",
                f"Yıl: {yil}",
                f"Sayı: {sayi}",
            ]
            dosya2_iade_infos.append(dosya2_iade_info)

        if not dosya2_iade_infos:
            return "Dosya2 İade bilgisi bulunmuyor"

        formatted_dosya2_iade_infos = "<br><br>".join(["<br>".join(info) for info in dosya2_iade_infos])
        return format_html(formatted_dosya2_iade_infos)

    def dosya2_iliski_list(self, obj):
        dosya2_iliski_infos = []

        for cocuk_dosya2iliski in obj.cocuk_dosya2iliski.all():
            yil = cocuk_dosya2iliski.yil if cocuk_dosya2iliski.yil else "Bilinmiyor"
            sayi = cocuk_dosya2iliski.sayi if cocuk_dosya2iliski.sayi else "Bilinmiyor"
            id = cocuk_dosya2iliski.id if cocuk_dosya2iliski.id else "Bilinmiyor"

            dosya2_iliski_info = [
                f"id: {id}",
                f"Yıl: {yil}",
                f"Sayı: {sayi}",
            ]
            dosya2_iliski_infos.append(dosya2_iliski_info)

        if not dosya2_iliski_infos:
            return "Dosya2 iliski bilgisi bulunmuyor"

        formatted_dosya2_iliski_infos = "<br><br>".join(["<br>".join(info) for info in dosya2_iliski_infos])
        return format_html(formatted_dosya2_iliski_infos)





    list_display = ['id', 'Adi', 'IkinciAdi','Soyadi','get_cinsiyet_display_icon', 'DogumTarihi', 'calculate_age', 'calculate_age1', 'age2', 'Yas16_Tarih',
                    'Yas19_Tarih', 'BabaAdi', 'AnneAdi', 'Ulkesi', 'dosya_list', 'dosya2_iade_list']  # Add 'age' or 'calculate_age' to display the age



    def get_cinsiyet_display_icon(self, obj):
        if obj.Cinsiyet == 'Erkek':
            return '👦'
        elif obj.Cinsiyet == 'Kadın':
            return '👧️'
        else:
            return obj.Cinsiyet
    get_cinsiyet_display_icon.short_description = 'Cinsiyet'
    get_cinsiyet_display_icon.admin_order_field = 'Cinsiyet'  # Use a sorting field in model
    get_cinsiyet_display_icon.sortable = True


admin.site.register(Cocuk, CocuklarAdmin)

# list_display = ['CocukID', 'Adi', 'Soyadi', 'DogumTarihi', 'calculate_age', 'calculate_age1', 'age2', 'Yas16_Tarih',
#                 'Yas19_Tarih', 'BabaAdi', 'AnneAdi', 'Ulkesi',
#                 'dosyalar_list']  # Add 'age' or 'calculate_age' to display the age
