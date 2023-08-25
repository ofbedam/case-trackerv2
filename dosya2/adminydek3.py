from dal import autocomplete
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import admin
from django_admin_multi_select_filter.filters import MultiSelectFieldListFilter
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from django import forms
from .models import DosyaCKIade, DosyaCKIliski, DosyaBilgi, Dosya1996, Dosya1980Velayet, CocugaBakimTurleri, CocuklaYakinlikTurleri, MahkemeRedNedenleri, NihaiSonucTurleri
from django.contrib.admin import RelatedFieldListFilter
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from django.contrib.admin.views.main import ChangeList
from django.db.models import Q
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.utils.encoding import smart_str
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import openpyxl as px
from openpyxl import Workbook
from yerler.models import Country
from django.contrib.admin import RelatedFieldListFilter
from django.db.models import F, Value
from django.db.models.functions import Concat

from django_admin_multi_select_filter.filters import MultiSelectFieldListFilter
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter


class Dosya_CK_Iade_AdminForm(forms.ModelForm):
    class Meta:
        model = DosyaCKIade
        fields = '__all__'
        widgets = {
            'Cocuklar': autocomplete.ModelSelect2Multiple(url='cocuklar-autocomplete'),
        }


    def clean(self):
        cleaned_data = super().clean()
        dosya_durumu = cleaned_data.get('DosyaDurumu')
        kapatma_tarihi = cleaned_data.get('DosyaKapatmaTarihi')

        if dosya_durumu == 'Kapalı' and not kapatma_tarihi:
            raise forms.ValidationError("Dosya kapatma tarihi girilmediği halde durum 'Kapalı' olarak seçilemez.")




class AuthorPublisherFilter(admin.SimpleListFilter):
    title = _('Gonderen VEYA YerineGetiren')
    parameter_name = 'gonderenVEYAyerinegetiren'

    def lookups(self, request, model_admin):
        ulkes = Country.objects.filter(Q(yerine_getiren_dosya2iade__isnull=False) | Q(gonderenulke_dosya2iade__isnull=False))
        return [(country.id,country.name) for country in ulkes]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(Q(GonderenUlke_id=value) | Q(YerineGetirenUlke_id=value))



@admin.register(DosyaCKIade)
class DosyaCKIadeAdmin(admin.ModelAdmin):
    form = Dosya_CK_Iade_AdminForm
    search_fields = ['yil', 'sayi', 'Cocuklar__Adi', 'Cocuklar__Soyadi']



    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ( 'yil', 'sayi')
        return self.readonly_fields

    def analyze_data_link(self, obj):
        url = reverse('admin:analyze_data')  # Use the admin namespace for the URL
        return format_html('<a href="{}?dosya_id={}">Analyze Data</a>', url, obj.id)

    analyze_data_link.short_description = 'Analyze Data'
    # Define the list display columns
    list_display = ['id', 'yil', 'sayi', 'aciklama',  'DosyaAcilisTarihi',
                    'DosyaKapatmaTarihi', 'DosyaDurumu', 'get_cocuklar']
    def get_cocuklar(self, obj):
        return ", ".join([cocuk.__str__() for cocuk in obj.Cocuklar.all()])

    get_cocuklar.short_description = 'Çocuklar'  # Set a custom column header



    list_filter = [
            AuthorPublisherFilter,
           ('DosyaDurumu', MultiSelectFieldListFilter),
           # ('GonderenUlke', RelatedDropdownFilter),
           #  ('YerineGetirenUlke', RelatedDropdownFilter),
        # ... other filters ...
    ]

    # Custom widget for multiselect
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple('GonderenUlke', is_stacked=False)},
    }

    list_display = (

        'yil',
        'sayi',
        'DosyaDurumu',
        'DosyaAcilisTarihi',
        'DosyaKapatmaTarihi',
        'aciklama',
        'GonderenUlke',
        'YerineGetirenUlke',
        'get_cocuklar'
    )

    def yerine_getiren_ulke(self, obj):
        return obj.YerineGetirenUlke if obj.dosyaiade else None

    yerine_getiren_ulke.short_description = 'YG-Ü'

    def gonderen_ulke(self, obj):
        return obj.GonderenUlke if obj.dosyaiade else None

    gonderen_ulke.short_description = 'Gön-Ü'




    def get_changeform_initial_data(self, request):
        initial_data = super().get_changeform_initial_data(request)
        latest_dosya = DosyaCKIade.objects.order_by('-yil', '-sayi').first()

        if latest_dosya:
            initial_data['yil'] = latest_dosya.yil
            initial_data['sayi'] = latest_dosya.sayi + 1
        else:
            initial_data['yil'] = 2023
            initial_data['sayi'] = 1




    # Custom admin action to save selected Dosyalar records as PDF
    def save_as_pdf_action(modeladmin, request, queryset):
        # Create a response object with PDF content type
        response = HttpResponse(content_type='application/pdf')
        # Set the filename for the PDF
        response['Content-Disposition'] = 'attachment; filename="dosyalar.pdf"'

        # Create a PDF canvas with specified encoding
        p = canvas.Canvas(response, pagesize=letter)

        # Register a font that supports Turkish characters (e.g., Arial Unicode MS)
        pdfmetrics.registerFont(TTFont('ArialUnicode', 'static/fonts/Arial_Unicode_MS.TTF'))
        # Use the registered font in the PDF canvas
        p.setFont("ArialUnicode", 12)

        for dosya in queryset:
            p.drawString(100, 700, f"Dosya ID: {dosya.id}")
            p.drawString(100, 680, f"Dosya Yıl: {dosya.yil}")
            p.drawString(100, 660, f"Dosya Sayı: {dosya.sayi}")
            p.drawString(100, 640, f"Dosya Durumu: {smart_str(dosya.DosyaDurumu)}")
            # p.drawString(100, 620, f"Dosya Durumu: { date}")

            # Add more fields as needed...

            p.showPage()

        p.save()

        return response

    save_as_pdf_action.short_description = "Seçili Dosyaları PDF olarak kaydet"


    def print_records(self, request, queryset):
        # Render the printable version of records as HTML
        printable_html = render_to_string('printable_records.html', {'queryset': queryset})

        # Create a response with HTML content type
        response = HttpResponse(content_type='text/html')
        response.write(printable_html)

        return response

    def export_as_excel(self, request, queryset):
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=secilidosyabilgisi.xlsx'
        workbook = Workbook()
        sheet = workbook.active

        # Add column headers
        column_headers = ['ID', 'Yıl', 'Sayı', 'Dosya Durumu', 'Açılış Tarihi', 'Kapanış Tarihi', 'Açıklama']
        sheet.append(column_headers)

        # Add data rows
        for obj in queryset:
            data_row = [obj.id, obj.yil, obj.sayi, obj.DosyaDurumu, obj.DosyaAcilisTarihi, obj.DosyaKapatmaTarihi, obj.aciklama]
            sheet.append(data_row)

        workbook.save(response)
        return response

    export_as_excel.short_description = "Seçili Dosyaları Excel olarak kaydet"

    actions = [export_as_excel, print_records, save_as_pdf_action]

#
#
# class DosyaIadeForm(forms.ModelForm):
#     class Meta:
#         model = DosyaIade
#         fields = '__all__'
#
#
#
#
#  # DOSYAIADE --- ADMIN ALANI
#
# class DosyaIadeAdminForm(forms.ModelForm):
#     class Meta:
#         model = DosyaIade
#         fields = '__all__'
#
#
# class DosyaIadeAdmin(admin.ModelAdmin):
#     form = DosyaIadeAdminForm
#     # list_display = [
#     #     'get_dosya_info',
#     #     'GonderenUlke',
#     #     'YerineGetirenUlke',
#     # ]
#     #
#     #
#     # def get_dosya_info(self, obj):
#     #     dosya = obj.dosya
#     #     cocuklar_list = ", ".join([cocuk.__str__() for cocuk in dosya.Cocuklar.all()])
#     #     return f"Dosya ID: {dosya.id}, Yil: {dosya.yil}, Sayı: {dosya.sayi}, Dosya Tür: {dosya.dosya_kodu}, Durum: {dosya.DosyaDurumu}, Cocuklar: {cocuklar_list}"
#     #
#     # get_dosya_info.short_description = 'Dosya Bilgileri'
#
#
#
#
#     # create a function in order to return a list of all DosyaIade records without exception
#
#
#
#
#     list_display = [
#         'dosya_id',
#         'dosya_yil',
#         'dosya_sayi',
#         'dosya_kodu',
#         'dosya_durumu',
#         'dosya_DosyaAcilisTarihi',
#         'dosya_DosyaKapatmaTarihi',
#         'dosya_cocuklar',
#         'f_GonderenUlke',
#         'f_YerineGetirenUlke',
#     ]
#
# # Create list_display for all
#
#
#
#     def f_GonderenUlke(self, obj):
#         return obj.GonderenUlke if obj.GonderenUlke else None
#     f_GonderenUlke.short_description = 'Gön.Ülke'
#
#     def f_YerineGetirenUlke(self, obj):
#         return obj.YerineGetirenUlke if obj.YerineGetirenUlke else None
#     f_YerineGetirenUlke.short_description = 'YG.Ülke'
#
#     def dosya_id(self, obj):
#         return obj.dosya.id
#
#     dosya_id.short_description = 'Dosya ID'
#
#     def dosya_DosyaAcilisTarihi(self, obj):
#         return obj.dosya.DosyaAcilisTarihi
#
#     dosya_DosyaAcilisTarihi.short_description = 'Aç.Tarihi'
#     def dosya_DosyaKapatmaTarihi(self, obj):
#         return obj.dosya.DosyaKapatmaTarihi
#
#     dosya_DosyaKapatmaTarihi.short_description = 'Kap.Tarihi'
#
#     def dosya_yil(self, obj):
#         return obj.dosya.yil
#
#     dosya_yil.short_description = 'Yıl'
#
#     def dosya_sayi(self, obj):
#         return obj.dosya.sayi
#
#     dosya_sayi.short_description = 'Sayı'
#
#     def dosya_kodu(self, obj):
#         return obj.dosya.dosya_kodu
#
#     dosya_kodu.short_description = 'Dosya Kodu'
#
#     def dosya_durumu(self, obj):
#         return obj.dosya.DosyaDurumu
#
#     dosya_durumu.short_description = 'Durum'
#
#     def dosya_cocuklar(self, obj):
#         return ", ".join([cocuk.__str__() for cocuk in obj.dosya.Cocuklar.all()])
#
#     dosya_cocuklar.short_description = 'Çocuklar'
#
#
#     def dosya_cocuk_adi(self, obj):
#         return ", ".join([cocuk.__str__() for cocuk in obj.dosya.Cocuklar.all()])
#
#     dosya_cocuk_adi.short_description = 'Çocuk'
#
#     list_filter = [
#         'dosya__yil',
#         'GonderenUlke',
#         'YerineGetirenUlke',
#
#     ]
#
#
#
# # Create a search function for the Cocuklar field including adi ve soyadi fields
# #     @admin.display(description='Çocuklar')
# #     def dosya_cocuklar_search(self, queryset, name, value):
# #         return queryset.filter(dosya__Cocuklar__cocuk_adi__icontains=value)
#
#     # @admin.display(description='Çocuklar')
#     # def dosya_cocuklar_search_soyadi(self, queryset, name, value):
#     #     return queryset.filter(dosya__Cocuklar__cocuk_soyadi__icontains=value)

    search_fields = ['yil', 'sayi','Cocuklar__Adi']

    # Disable add view
    # def has_add_permission(self, request):
    #     return False
   # def has_add_permission(self, request):
    #     return False

    def has_change_permission(self, request, obj=None):
        return False
        # Disable Dosya field in the list view

    # def dosya(self, obj):
    #     return obj.dosya.dosya_kodu

# admin.site.register(DosyaCKIadeAdmin)




@admin.register(DosyaCKIliski)
class DosyaCKIliskiAdmin(admin.ModelAdmin):
    form = DosyaCKIliskiAdmin
    search_fields = ['yil', 'sayi', 'Cocuklar__Adi', 'Cocuklar__Soyadi']



    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ( 'yil', 'sayi')
        return self.readonly_fields
class DosyaCKIliskiAdminForm(forms.ModelForm):
    class Meta:
        model = DosyaCKIliski
        fields = '__all__'
        widgets = {
            'Cocuklar': autocomplete.ModelSelect2Multiple(url='cocuklar-autocomplete'),
        }




admin.site.register(CocugaBakimTurleri)
admin.site.register(CocuklaYakinlikTurleri)
admin.site.register(MahkemeRedNedenleri)
admin.site.register(NihaiSonucTurleri)
