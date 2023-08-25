# yerler/admin.py

from django.contrib import admin

# Register your models here.

from .models import Country,  State, City




class CityAdmin(admin.ModelAdmin):
    search_fields = ['name', 'state', 'country']
    # list_display = ('__str__',)  # This displays the custom representation from the __str__ method.
    list_display = ['id', 'custom_name', 'custom_state', 'custom_country']
    list_filter = ['country', 'state']

    def custom_name(self, obj):
        return obj.name  # Customize this method if needed

    custom_name.short_description = 'Adı'

    def custom_state(self, obj):
        return obj.state.name if obj.state else None  # Customize this method if needed

    custom_state.short_description = 'Şehir/Eyalet'

    def custom_country(self, obj):
        return obj.country.name if obj.country else None  # Customize this method if needed

    custom_country.short_description = 'Ülke'


class StateAdmin(admin.ModelAdmin):
    # list_display = ('__str__',)  # This displays the custom representation from the __str__ method.
    search_fields = ['name']
    list_display = ['id', 'custom_name', 'custom_country']
    list_filter = ['country']

    def custom_name(self, obj):
        return obj.name  # Customize this method if needed

    custom_name.short_description = 'Adı'

    def custom_state(self, obj):
        return obj.state.name if obj.state else None  # Customize this method if needed

    custom_state.short_description = 'Şehir/Eyalet'

    def custom_country(self, obj):
        return obj.country.name if obj.country else None  # Customize this method if needed

    custom_country.short_description = 'Ülke'

class CountryAdmin(admin.ModelAdmin):
        # list_display = ('__str__',)  # This displays the custom representation from the __str__ method.
        search_fields = ['name']
        list_display = ['id', 'custom_name']

        def custom_name(self, obj):
            return obj.name  # Customize this method if needed

        custom_name.short_description = 'Adı'



admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)


