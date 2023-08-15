from django.contrib import admin
from .models import Dosyalar
from kisiler.models import Kisiler
from dal import autocomplete
from django import forms


class DosyalarAdminForm(forms.ModelForm):
    class Meta:
        model = Dosyalar
        fields = '__all__'
        widgets = {
            'Cocuklar': autocomplete.ModelSelect2Multiple(url='cocuklar-autocomplete'),
            'DosyaTuru': forms.Select(),
            'DosyaKodu': forms.Select(attrs={'disabled': 'disabled'}),  # Disable DosyaKodu field
            'DosyaYil': forms.TextInput(attrs={'readonly': True}),  # Bu alanı etkin olmaktan çıkarır
            'DosyaNo': forms.NumberInput(),  # Bu alanı görünür ve etkin hale getirir
        }

    basvurucu = forms.ModelChoiceField(queryset=Kisiler.objects.all(), label='Başvurucu', widget=autocomplete.ModelSelect2(url='kisiler-autocomplete'))
    karsi_taraf = forms.ModelChoiceField(queryset=Kisiler.objects.all(), label='Karşı Taraf', widget=autocomplete.ModelSelect2(url='kisiler-autocomplete'))

def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_year = datetime.now().year
        self.fields['DosyaYil'].initial = current_year  # Set default value for DosyaYil
        self.fields['DosyaNo'].widget.attrs['readonly'] = False  # Enable DosyaNo field


class DosyalarAdmin(admin.ModelAdmin):
    form = DosyalarAdminForm

# admin.site.register(Dosyalar, DosyalarAdmin)