from dal import autocomplete
from django.template.loader import render_to_string
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from django.urls import reverse
from django.utils.html import format_html

from django.contrib import admin
from django import forms

from .models import Dosya, DosyaIliski, DosyaIade, DosyaBilgi, Dosya1996, Dosya1980Velayet, CocugaBakimTurleri, CocuklaYakinlikTurleri, MahkemeRedNedenleri, NihaiSonucTurleri, Dosya1980CK

from django.contrib.admin import RelatedFieldListFilter

from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from django.utils.encoding import smart_str
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import openpyxl as px
from openpyxl import Workbook

from yerler.models import Country


from django.contrib.admin import RelatedFieldListFilter



class DosyaIliskiInline(admin.StackedInline):  # veya admin.TabularInline
    model = DosyaIliski  # İlgili inline model
    extra = 1  # Kaç adet boş form alanı gösterileceği

class DosyaIadeInline(admin.StackedInline):  # veya admin.TabularInline
    model = DosyaIade  # İlgili inline model
    extra = 1  # Kaç adet boş form alanı gösterileceği

class Dosya1996Inline(admin.StackedInline):  # veya admin.TabularInline
    model = Dosya1996  # İlgili inline model
    extra = 1  # Kaç adet boş form alanı gösterileceği7

class Dosya1980VelayetInline(admin.StackedInline):  # veya admin.TabularInline
    model = Dosya1980Velayet  # İlgili inline model
    extra = 1  # Kaç adet boş form alanı gösterileceği

class DosyaBilgiInline(admin.StackedInline):  # veya admin.TabularInline
    model = DosyaBilgi  # İlgili inline model
    extra = 1  # Kaç adet boş form alanı gösterileceği



class DosyaAdminForm(forms.ModelForm):
    class Meta:
        model = Dosya
        fields = '__all__'
        widgets = {
            'Cocuklar': autocomplete.ModelSelect2Multiple(url='cocuklar-autocomplete'),
        }


    def clean(self):
        cleaned_data = super().clean()
        dosya_kodu = cleaned_data.get('dosya_kodu')
        yil = cleaned_data.get('yil')
        sayi = cleaned_data.get('sayi')

        if dosya_kodu in ['A', 'B', 'C']:
            existing_dosya = Dosya.objects.filter(
                dosya_kodu__in=['A', 'B', 'C'],
                yil=yil,
                sayi=sayi,
            ).exclude(pk=self.instance.pk).first()

            if existing_dosya:
                raise forms.ValidationError(
                    f"[dosya_kodu= {dosya_kodu} y={yil} / s={sayi}] ile [dosya_kodu= {existing_dosya.dosya_kodu} Yil={existing_dosya.yil} ve Sayi={existing_dosya.sayi}] mükerrerdir."
                )

        elif dosya_kodu in ['D']:
            existing_dosya = Dosya.objects.filter(
                dosya_kodu='D',
                yil=yil,
                sayi=sayi,
            ).exclude(pk=self.instance.pk).first()

            if existing_dosya:
                raise forms.ValidationError(
                    f"[dosya_kodu= {dosya_kodu} zYil={yil} ve Sayi={sayi}] ile [dosya_kodu= {existing_dosya.dosya_kodu} Yil={existing_dosya.yil} ve Sayi={existing_dosya.sayi}] mükerrerdir."
                )

        elif dosya_kodu in ['E']:
            existing_dosya = Dosya.objects.filter(
                dosya_kodu='E',
                yil=yil,
                sayi=sayi,
            ).exclude(pk=self.instance.pk).first()

            if existing_dosya:
                raise forms.ValidationError(
                    f"[dosya_kodu= {dosya_kodu}  bbb Yil={yil} ve Sayi={sayi}] ile [dosya_kodu= {existing_dosya.dosya_kodu} Yil={existing_dosya.yil} ve Sayi={existing_dosya.sayi}] mükerrerdir."
                )

        dosya_durumu = cleaned_data.get('DosyaDurumu')
        kapatma_tarihi = cleaned_data.get('DosyaKapatmaTarihi')

        if dosya_durumu == 'Kapalı' and not kapatma_tarihi:
            raise forms.ValidationError("Dosya kapatma tarihi girilmediği halde durum 'Kapalı' olarak seçilemez.")



@admin.register(Dosya)
class DosyaAdmin(admin.ModelAdmin):
    form = DosyaAdminForm
    search_fields = ['yil', 'sayi', 'Cocuklar__Adi', 'Cocuklar__Soyadi']

    # def get_readonly_fields(self, request, obj=None):
    #     readonly_fields = list(self.readonly_fields)
    #     if obj and obj.pk:
    #         # If object is being edited (not during creation), add DosyaTuru to readonly_fields
    #         readonly_fields.append('DosyaTuru')
    #     return readonly_fields

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('dosya_kodu', 'yil', 'sayi')
        return self.readonly_fields

    def analyze_data_link(self, obj):
        url = reverse('admin:analyze_data')  # Use the admin namespace for the URL
        return format_html('<a href="{}?dosya_id={}">Analyze Data</a>', url, obj.id)

    analyze_data_link.short_description = 'Analyze Data'
    # Define the list display columns
    list_display = ['id', 'dosya_kodu', 'yil', 'sayi', 'aciklama',  'DosyaAcilisTarihi',
                    'DosyaKapatmaTarihi', 'DosyaDurumu', 'get_cocuklar']
    def get_cocuklar(self, obj):
        return ", ".join([cocuk.__str__() for cocuk in obj.Cocuklar.all()])

    get_cocuklar.short_description = 'Çocuklar'  # Set a custom column header

    # class YerineGetirenUlkeFilter(SimpleListFilter):
    #     title = _('Yerine Getiren Ülke')
    #     parameter_name = 'yerine_getiren_ulke'
    #
    #     def lookups(self, request, model_admin):
    #         queryset = model_admin.get_queryset(request)
    #         return [(obj.yerine_getiren_dosyaiade.id, obj.yerine_getiren_dosyaiade) for obj in queryset if
    #                 obj.yerine_getiren_dosyaiade]
    #
    #     def queryset(self, request, queryset):
    #         value = self.value()
    #         if value:
    #             return queryset.filter(yerine_getiren_dosyaiade=value)


    #
    # # Define the list filter options for specific fields
    # list_filter = [
    #     'yil',
    #     'dosya_kodu',
    #     'DosyaDurumu',
    #     # 'dosyaiade__YerineGetirenUlke',
    #
    #     ('dosyaiade__YerineGetirenUlke', RelatedFieldListFilter),
    #     # 'dosyaiade__GonderenUlke',
    #     # 'dosyailiski__GonderenUlke',
    #     # 'dosyailiski__YerineGetirenUlke',
    #
    # ] # iade__YerineGetirenUlke kullanıyoruz
    # # def get_queryset(self, request):
    # #     queryset = super().get_queryset(request)
    # #     return queryset.select_related(
    # #         'dosyaiade__YerineGetirenUlke',
    # #         'dosyaiade__GonderenUlke',
    # #         'dosyailiski__GonderenUlke',
    # #         'dosyailiski__YerineGetirenUlke'
    #     )

    # list_filter = [
    #     ('dosyaiade__YerineGetirenUlke', RelatedFieldListFilter),
    # ]

    class CustomRelatedFieldListFilter(RelatedFieldListFilter):
        def field_choices(self, field, request, model_admin):
            choices = field.get_choices(include_blank=False, limit_choices_to=field.get_limit_choices_to())
            sorted_choices = sorted(choices, key=lambda x: x[1])  # Seçenekleri alfabetik olarak sırala
            return sorted_choices


    list_filter = [
        ('DosyaDurumu', admin.ChoicesFieldListFilter),
        ('dosya_kodu', admin.ChoicesFieldListFilter),
        ('dosyaiade__GonderenUlke', CustomRelatedFieldListFilter),
        ('dosyaiade__YerineGetirenUlke', admin.RelatedFieldListFilter),
        # ('dosyaiade__GonderenUlke', admin.RelatedFieldListFilter),

    ]

    list_display = (
        'dosya_kodu',
        'yil',
        'sayi',
        'DosyaDurumu',
        'DosyaAcilisTarihi',
        'DosyaKapatmaTarihi',
        'aciklama',
        'iade_yerine_getiren_ulke',  # Metot tarafından döndürülen değer burada gösterilecek
        'iade_gonderen_ulke',
    )

    def iade_yerine_getiren_ulke(self, obj):
        return obj.dosyaiade.YerineGetirenUlke if obj.dosyaiade else None

    iade_yerine_getiren_ulke.short_description = 'İade-YG-Ülke'

    def iade_gonderen_ulke(self, obj):
        return obj.dosyaiade.GonderenUlke if obj.dosyaiade else None

    iade_gonderen_ulke.short_description = 'İade-Gön-Ülke'


    # inlines = [DosyaIliskiInline, DosyaIadeInline, Dosya1980VelayetInline, Dosya1996Inline,DosyaBilgiInline]
    change_form_template = 'admin/dosya_change_form.html'
    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []

        dosya_kodu = obj.dosya_kodu
        if dosya_kodu == 'A':
            return [DosyaIadeInline(self.model, self.admin_site)]
        elif dosya_kodu == 'B':
            return [DosyaIliskiInline(self.model, self.admin_site)]
        elif dosya_kodu == 'C':
            return [Dosya1996Inline(self.model, self.admin_site)]
        elif dosya_kodu == 'D':
            return [Dosya1980VelayetInline(self.model, self.admin_site)]
        elif dosya_kodu == 'E':
            return [DosyaBilgiInline(self.model, self.admin_site)]

        return []

    def add_view(self, request, form_url='', extra_context=None):
        # Form ekranı yüklendiğinde, formset'in TOTAL_FORMS ve INITIAL_FORMS değerlerini belirtin
        if extra_context is None:
            extra_context = {}
        extra_context['dosyaiade-TOTAL_FORMS'] = 1  # İlk yüklemede 1 form gösterilecek
        extra_context['dosyaiade-INITIAL_FORMS'] = 0  # İlk yüklemede boş form

        latest_values = []

        dosya_kodlari = ['A', 'B', 'C', 'D', 'E']  # Tüm dosya kodları

        for dosya_kodu in dosya_kodlari:
            yil, sayi = Dosya.get_latest_yil_sayi(dosya_kodu)
            dosya_kodu_adi = dict(Dosya.DOSYA_KODLARI).get(dosya_kodu)

            if yil is not None and sayi is not None:
                latest_values.append({
                    'dosya_kodu': dosya_kodu,
                    'dosya_kodu_adi': dosya_kodu_adi,
                    'yil': yil,
                    'sayi': sayi,
                })

        latest_dosya_id = []

        dosya_kodlari = ['A', 'B', 'C', 'D', 'E']  # Tüm dosya kodları

        for dosya_kodu in dosya_kodlari:
            yil, sayi = Dosya.get_latest_dosya_id(dosya_kodu)
            dosya_kodu_adi = dict(Dosya.DOSYA_KODLARI).get(dosya_kodu)

            if yil is not None and sayi is not None:
                latest_dosya_id.append({
                    'dosya_kodu': dosya_kodu,
                    'dosya_kodu_adi': dosya_kodu_adi,
                    'yil': yil,
                    'sayi': sayi,
                })
        extra_context['latest_dosya_id'] = latest_dosya_id
        extra_context['latest_values'] = latest_values
        return super().add_view(request, form_url=form_url, extra_context=extra_context)





    def get_changeform_initial_data(self, request):
        initial_data = super().get_changeform_initial_data(request)
        latest_dosya = Dosya.objects.order_by('-yil', '-sayi').first()

        if latest_dosya:
            initial_data['yil'] = latest_dosya.yil
            initial_data['sayi'] = latest_dosya.sayi + 1
        else:
            initial_data['yil'] = 2022
            initial_data['sayi'] = 1



        latest_values = []

        dosya_kodlari = ['A', 'B', 'C', 'D', 'E']  # Tüm dosya kodları

        for dosya_kodu in dosya_kodlari:
            yil, sayi = Dosya.get_latest_yil_sayi(dosya_kodu)
            dosya_kodu_adi = dict(Dosya.DOSYA_KODLARI).get(dosya_kodu)

            if yil is not None and sayi is not None:
                latest_values.append(f"[dosya_kodu= {dosya_kodu_adi} Yil={yil} ve Sayi={sayi}]")

        initial_data['latest_values'] = '\n'.join(latest_values)
        return initial_data



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



class DosyaIadeForm(forms.ModelForm):
    class Meta:
        model = DosyaIade
        fields = '__all__'

# @admin.register(DosyaIade)
# class DosyaIadeAdmin(admin.ModelAdmin):
#     form = DosyaIadeForm
#     fieldsets = (
#         ('Dosya Bilgileri', {
#             'fields': ('dosya', 'neden')
#         }),
#         # ('Ek Bilgiler', {
#         #     'fields': ('diger_alan1', 'diger_alan2'),
#         #     'classes': ('collapse',)
#         # }),
#     )
#
#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         if obj:
#             form.base_fields['dosya'].disabled = True
#         return form
#
#
#
#
# class DosyaIadeAdminForm(forms.ModelForm):
#     dosya_kodu = forms.ChoiceField(choices=[(dosya.dosya_kodu, str(dosya)) for dosya in Dosya.objects.all()])
#
#     class Meta:
#         model = DosyaIade
#         fields = '__all__'
#
# @admin.register(DosyaIade)
# class DosyaIadeAdmin(admin.ModelAdmin):
#     form = DosyaIadeAdminForm


#
# class DosyaIadeAdminForm(forms.ModelForm):
#     yil = forms.IntegerField(widget=forms.HiddenInput())
#
#     sayi = forms.IntegerField()
#     aciklama = forms.CharField(widget=forms.Textarea, required=False)
#     neden = forms.CharField(max_length=50)
#
#
#
#     class Meta:
#         model = DosyaIade
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.initial['yil'] = self.instance.dosya.yil  # Dosya kaydının yil alanını alıp form alanına atar
# @admin.register(DosyaIade)
# class DosyaIadeAdmin(admin.ModelAdmin):
#     form = DosyaIadeAdminForm


from django.contrib import admin
from .models import DosyaIade
from django.contrib import admin
from django_admin_multi_select_filter.filters import MultiSelectFieldListFilter

class DosyaIadeAdmin(admin.ModelAdmin):
    # list_display = [
    #     'get_dosya_info',
    #     'GonderenUlke',
    #     'YerineGetirenUlke',
    # ]
    #
    #
    # def get_dosya_info(self, obj):
    #     dosya = obj.dosya
    #     cocuklar_list = ", ".join([cocuk.__str__() for cocuk in dosya.Cocuklar.all()])
    #     return f"Dosya ID: {dosya.id}, Yil: {dosya.yil}, Sayı: {dosya.sayi}, Dosya Tür: {dosya.dosya_kodu}, Durum: {dosya.DosyaDurumu}, Cocuklar: {cocuklar_list}"
    #
    # get_dosya_info.short_description = 'Dosya Bilgileri'

    list_display = [
        'dosya_id',
        'dosya_yil',
        'dosya_sayi',
        'dosya_kodu',
        'dosya_durumu',
        'dosya_DosyaAcilisTarihi',
        'dosya_DosyaKapatmaTarihi',
        'dosya_cocuklar',
        'f_GonderenUlke',
        'f_YerineGetirenUlke',
    ]

    def f_GonderenUlke(self, obj):
        return obj.GonderenUlke
    f_GonderenUlke.short_description = 'Gön.Ülke'

    def f_YerineGetirenUlke(self, obj):
        return obj.YerineGetirenUlke
    f_YerineGetirenUlke.short_description = 'YG.Ülke'

    def dosya_id(self, obj):
        return obj.dosya.id

    dosya_id.short_description = 'Dosya ID'

    def dosya_DosyaAcilisTarihi(self, obj):
        return obj.dosya.DosyaAcilisTarihi

    dosya_DosyaAcilisTarihi.short_description = 'Aç.Tarihi'
    def dosya_DosyaKapatmaTarihi(self, obj):
        return obj.dosya.DosyaKapatmaTarihi

    dosya_DosyaKapatmaTarihi.short_description = 'Kap.Tarihi'

    def dosya_yil(self, obj):
        return obj.dosya.yil

    dosya_yil.short_description = 'Yıl'

    def dosya_sayi(self, obj):
        return obj.dosya.sayi

    dosya_sayi.short_description = 'Sayı'

    def dosya_kodu(self, obj):
        return obj.dosya.dosya_kodu

    dosya_kodu.short_description = 'Dosya Kodu'

    def dosya_durumu(self, obj):
        return obj.dosya.DosyaDurumu

    dosya_durumu.short_description = 'Durum'

    def dosya_cocuklar(self, obj):
        return ", ".join([cocuk.__str__() for cocuk in obj.dosya.Cocuklar.all()])

    dosya_cocuklar.short_description = 'Çocuklar'

    list_filter = [
        'dosya__yil',
        ('GonderenUlke', MultiSelectFieldListFilter),
        'YerineGetirenUlke',

    ]

    search_fields = ['dosya__dosya_kodu', 'GonderenUlke__name', 'YerineGetirenUlke__name']

    # Disable add view
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
        # Disable Dosya field in the list view

    def dosya(self, obj):
        return obj.dosya.dosya_kodu

admin.site.register(DosyaIade, DosyaIadeAdmin)








admin.site.register(CocugaBakimTurleri)
admin.site.register(CocuklaYakinlikTurleri)
admin.site.register(MahkemeRedNedenleri)
admin.site.register(NihaiSonucTurleri)
admin.site.register(Dosya1980CK)