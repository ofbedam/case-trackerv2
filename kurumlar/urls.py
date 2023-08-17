# kurumlar/urls.py


from . import views
from django.urls import path


urlpatterns = [

    path('country-autocomplete/', views.CountryAutocomplete.as_view(), name='country-autocomplete'),
    path('state-autocomplete/', views.StateAutocomplete.as_view(), name='state-autocomplete'),
    path('city-autocomplete/', views.CityAutocomplete.as_view(), name='city-autocomplete'),
]
