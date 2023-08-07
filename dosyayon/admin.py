from django.contrib import admin
from dosyayon.models import Country,  State, City

from django import forms
from dal import autocomplete
from django.template.loader import render_to_string
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
class CityAdmin(admin.ModelAdmin):
    search_fields = ['name', 'state', 'country']
    # list_display = ('__str__',)  # This displays the custom representation from the __str__ method.
    list_display = ['name', 'state', 'country']


class StateAdmin(admin.ModelAdmin):
    # list_display = ('__str__',)  # This displays the custom representation from the __str__ method.
    search_fields = ['name']
    list_display = ['name', 'country']

class CountryAdmin(admin.ModelAdmin):
        # list_display = ('__str__',)  # This displays the custom representation from the __str__ method.
        search_fields = ['name']
        list_display = ['name']

admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)


