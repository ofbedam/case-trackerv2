# # #kurumlar/forms.py


from django import forms
from dal import autocomplete
from yerler.models import Country, State, City
from .models import Kurumlar

class KurumlarForm(forms.ModelForm):
    Country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        widget=autocomplete.ModelSelect2(url='country-autocomplete')
    )

    State = forms.ModelChoiceField(
        queryset=State.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='state-autocomplete',
            forward=['Country']
        )
    )

    City = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='city-autocomplete',
            forward=['State']
        )
    )

    class Meta:
        model = Kurumlar
        fields = "__all__"
