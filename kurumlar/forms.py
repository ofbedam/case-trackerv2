#kurumlar/forms.py

from django import forms
from smart_selects.form_fields import ChainedModelChoiceField
from yerler.models import Country, State, City
from .models import Kurumlar
from django_select2.forms import ModelSelect2Widget

class KurumlarForm(forms.ModelForm):
    UlkeID = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        widget=ModelSelect2Widget(
            queryset=Country.objects.all(),
            search_fields=['name__icontains'],
            attrs={'data-placeholder': 'Select a country'}
        )
    )

    State = forms.ModelChoiceField(
        queryset=State.objects.all(),
        widget=ModelSelect2Widget(
            queryset=State.objects.all(),
            search_fields=['name__icontains'],
            dependent_fields={'City': 'City'},
            attrs={'data-placeholder': 'Select a state'}
        )
    )

    City = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=ModelSelect2Widget(
            queryset=City.objects.all(),
            search_fields=['name__icontains'],
            attrs={'data-placeholder': 'Select a city'}
        )
    )

    class Meta:
        model = Kurumlar
        fields = "__all__"

#
#
