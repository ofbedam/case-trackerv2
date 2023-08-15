# dosyayon/forms.py
from django.contrib import admin
from .models import Dosyalar, Cocuklar, Kisiler
from dal import autocomplete
from django import forms






from django import forms
from django.shortcuts import render
from .models import Country, State, City

class LocationForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Select Country")
    state = forms.ModelChoiceField(queryset=State.objects.none(), empty_label="Select State")
    city = forms.ModelChoiceField(queryset=City.objects.none(), empty_label="Select City")

def location(request):
    form = LocationForm()

    if request.method == 'POST':
        form = LocationForm(request.POST)

        if form.is_valid():
            country_id = form.cleaned_data['country'].id
            state_queryset = State.objects.filter(country_id=country_id)
            form.fields['state'].queryset = state_queryset

            state_id = form.cleaned_data['state'].id
            city_queryset = City.objects.filter(state_id=state_id)
            form.fields['city'].queryset = city_queryset

    return render(request, 'location.html', {'form': form})
