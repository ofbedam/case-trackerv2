# yerler/views.py
from dal import autocomplete
from .models import Country, State, City

class StateAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        country_id = self.forwarded.get('country', None)
        if country_id:
            return State.objects.filter(country_id=country_id)
        return State.objects.none()

class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        state_id = self.forwarded.get('state', None)
        if state_id:
            return City.objects.filter(state_id=state_id)
        return City.objects.none()
