from dal import autocomplete
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import admin
from django_admin_multi_select_filter.filters import MultiSelectFieldListFilter
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from django import forms
from .models import DosyaCKIliski
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
from .models import DosyaCKIliski
from dosya2.models import  DosyaBilgi, Dosya1996, Dosya1980Velayet, CocugaBakimTurleri, CocuklaYakinlikTurleri, MahkemeRedNedenleri, NihaiSonucTurleri
from django.contrib.admin import RelatedFieldListFilter

class DosyaCKIliskiAdminForm(forms.ModelForm):
    class Meta:
        model = DosyaCKIliski

        fields = '__all__'
        widgets = {
            'Cocuklar': autocomplete.ModelSelect2Multiple(url='cocuklar-autocomplete'),
        }




@admin.register(DosyaCKIliski)
class DosyaCKIliskiAdmin(admin.ModelAdmin):
    form = DosyaCKIliskiAdminForm
    class DosyaCKIAdmin(admin.ModelAdmin):
        def get_changeform_initial_data(self, request):
            initial_data = super().get_changeform_initial_data(request)

            # Get the highest value of 'sayi' and 'yil' from both models
            highest_sayi_liski = DosyaCKIliski.objects.order_by('-sayi').first()
            highest_sayi_ade = DosyaCKIliski.objects.order_by('-sayi').first()

            highest_sayi = max(
                highest_sayi_liski.sayi if highest_sayi_liski else 0,
                highest_sayi_ade.sayi if highest_sayi_ade else 0
            )

            # Get the current year
            current_year = datetime.datetime.now().year

            initial_data['yil'] = current_year
            initial_data['sayi'] = highest_sayi + 1

            return initial_data

    search_fields = ['yil', 'sayi', 'Cocuklar__Adi', 'Cocuklar__Soyadi']



    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ( 'yil', 'sayi')
        return self.readonly_fields

    def get_cocuklar(self, obj):
        return ", ".join([cocuk.__str__() for cocuk in obj.Cocuklar.all()])

    get_cocuklar.short_description = 'Çocuklar'  # Set a custom column header
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

