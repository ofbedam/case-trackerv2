#kurumlar/views.py

from dal import autocomplete
from yerler.models import Country, State, City

class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Country.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class StateAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = State.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
