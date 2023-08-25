from dal import autocomplete
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import admin
from django_admin_multi_select_filter.filters import MultiSelectFieldListFilter
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from django import forms
from .models import DosyaBilgi, Dosya1996, Dosya1980Velayet, CocugaBakimTurleri, CocuklaYakinlikTurleri, MahkemeRedNedenleri, NihaiSonucTurleri
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
from .dosyaiade.admin import  DosyaCKIadeAdmin
from .dosyailiski.admin import DosyaCKIliski
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



admin.site.register(CocugaBakimTurleri)
admin.site.register(CocuklaYakinlikTurleri)
admin.site.register(MahkemeRedNedenleri)
admin.site.register(NihaiSonucTurleri)
