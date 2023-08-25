from dal import autocomplete
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import admin
from django_admin_multi_select_filter.filters import MultiSelectFieldListFilter
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from django import forms
from .models import DosyaCKIade
from ..dosyailiski.models import DosyaCKIliski
from dosya2.models import  DosyaBilgi, Dosya1996, Dosya1980Velayet, CocugaBakimTurleri, CocuklaYakinlikTurleri, MahkemeRedNedenleri, NihaiSonucTurleri
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

#
# class DosyaIliskiInline(admin.StackedInline):  # veya admin.TabularInline
#     model = DosyaCKIliski  # İlgili inline model
#     extra = 1  # Kaç adet boş form alanı gösterileceği
#
# class DosyaIadeInline(admin.StackedInline):  # veya admin.TabularInline
#     model = DosyaCKIade  # İlgili inline model
#     extra = 1  # Kaç adet boş form alanı gösterileceği
#
# class Dosya1996Inline(admin.StackedInline):  # veya admin.TabularInline
#     model = Dosya1996  # İlgili inline model
#     extra = 1  # Kaç adet boş form alanı gösterileceği7
#
# class Dosya1980VelayetInline(admin.StackedInline):  # veya admin.TabularInline
#     model = Dosya1980Velayet  # İlgili inline model
#     extra = 1  # Kaç adet boş form alanı gösterileceği
#
# class DosyaBilgiInline(admin.StackedInline):  # veya admin.TabularInline
#     model = DosyaBilgi  # İlgili inline model
#     extra = 1  # Kaç adet boş form alanı gösterileceği
#




search_fields = ['yil', 'sayi', 'Cocuklar__Adi', 'Cocuklar__Soyadi']
class DosyaCKIadeAdminForm(forms.ModelForm):
    class Meta:
        model = DosyaCKIade
        fields = '__all__'
        widgets = {
            'Cocuklar': autocomplete.ModelSelect2Multiple(url='cocuklar-autocomplete'),
            'basvurucu': autocomplete.ModelSelect2Multiple(url='kisiler-autocomplete'),
            'karsi_taraf': autocomplete.ModelSelect2Multiple(url='kisiler-autocomplete'),
            'GonderenUlke': autocomplete.ModelSelect2Multiple(url='CountryAutocomplete'),
            'YerineGetirenUlke': autocomplete.ModelSelect2Multiple(url='CountryAutocomplete'),
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
    form = DosyaCKIadeAdminForm

    def get_changeform_initial_data(self, request):
        initial_data = super().get_changeform_initial_data(request)
        latest_dosya = DosyaCKIliski.objects.order_by('-yil', '-sayi').first()

        if latest_dosya:
            initial_data['yil'] = latest_dosya.yil
            initial_data['sayi'] = latest_dosya.sayi + 1
        else:
            initial_data['yil'] = 2023
            initial_data['sayi'] = 1

        return initial_data





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


    class CustomRelatedFieldListFilter(RelatedFieldListFilter):
        def field_choices(self, field, request, model_admin):
            choices = field.get_choices(include_blank=False, limit_choices_to=field.get_limit_choices_to())
            sorted_choices = sorted(choices, key=lambda x: x[1])  # Seçenekleri alfabetik olarak sırala
            return sorted_choices
 # create multiselect widget for  the items in list_filter



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

    # def print_dosyalar(modeladmin, request, queryset):
    #     # Custom admin action for "Print"
    #     html = render_to_string('dosyalar_pdf.html', {'dosyalar_list': queryset})
    #     return HttpResponse(html)
    # print_dosyalar.short_description = "Print"



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


    search_fields = ['yil', 'sayi','Cocuklar__Adi']

    # Disable add view
    # def has_add_permission(self, request):
    #     return False
   # def has_add_permission(self, request):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False
        # Disable Dosya field in the list view

    # def dosya(self, obj):
    #     return obj.dosya.dosya_kodu

# admin.site.register(DosyaCKIadeAdmin)

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ( 'yil', 'sayi')
        return self.readonly_fields


