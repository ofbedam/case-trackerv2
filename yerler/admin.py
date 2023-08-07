from django.contrib import admin

# Register your models here.

from .models import Country,  State, City

class CityAdmin(admin.ModelAdmin):
    search_fields = ['name', 'state', 'country']
    # list_display = ('__str__',)  # This displays the custom representation from the __str__ method.
    list_display = ['id','name', 'state', 'country']


class StateAdmin(admin.ModelAdmin):
    # list_display = ('__str__',)  # This displays the custom representation from the __str__ method.
    search_fields = ['name']
    list_display = ['id','name', 'country']

class CountryAdmin(admin.ModelAdmin):
        # list_display = ('__str__',)  # This displays the custom representation from the __str__ method.
        search_fields = ['name']
        list_display = ['id','name']

admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)


