import django_filters
from .models import DosyaIade
from yerler.models import Country
class DosyaIadeFilter(django_filters.FilterSet):
    GonderenUlke = django_filters.ModelMultipleChoiceFilter(queryset=Country.objects.all())
    YerineGetirenUlke = django_filters.ModelMultipleChoiceFilter(queryset=Country.objects.all())

    class Meta:
        model = DosyaIade
        fields = ['GonderenUlke', 'YerineGetirenUlke']

