# dosyayon/forms.py
from django.contrib import admin
from .models import Dosyalar, Cocuklar, Kisiler
from dal import autocomplete
from django import forms

class DosyalarAdminForm(forms.ModelForm):
    class Meta:
        model = Dosyalar
        fields = '__all__'
        widgets = {
            'CocukID': autocomplete.ModelSelect2Multiple(
                url='cocuklar-autocomplete',  # Replace this with the URL pattern for CocuklarAutocomplete view
            )
        }

    basvurucu = forms.ModelChoiceField(queryset=Kisiler.objects.all(), label='Başvurucu', widget=autocomplete.ModelSelect2(url='kisiler-autocomplete'))
    karsi_taraf = forms.ModelChoiceField(queryset=Kisiler.objects.all(), label='Karşı Taraf', widget=autocomplete.ModelSelect2(url='kisiler-autocomplete'))




class DosyalarAdmin(admin.ModelAdmin):
    form = DosyalarAdminForm

admin.site.register(Dosyalar, DosyalarAdmin)


class CocuklarAdminForm(forms.ModelForm):
    class Meta:
        model = Cocuklar
        fields = '__all__'
        widgets = {
            'AnneAdi': autocomplete.ModelSelect2(url='kisiler-autocomplete'),
            'BabaAdi': autocomplete.ModelSelect2(url='kisiler-autocomplete'),
        }


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
