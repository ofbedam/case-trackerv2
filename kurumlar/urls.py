#kurumlar/urls.py
from django.urls import path
from .views import CountryAutocomplete, StateAutocomplete, CityAutocomplete


urlpatterns = [
    path('country-autocomplete/', CountryAutocomplete.as_view(), name='country-autocomplete'),
    path('state-autocomplete/', StateAutocomplete.as_view(), name='state-autocomplete'),
    path('city-autocomplete/', CityAutocomplete.as_view(), name='city-autocomplete'),



]
