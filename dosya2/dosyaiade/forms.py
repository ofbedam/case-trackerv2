from django import forms
from .models import Dosya, DosyaIade, DosyaIliski

class DosyaForm(forms.ModelForm):
    class Meta:
        model = Dosya
        # fields = ('DosyaKodu', 'Yil', 'Sayi')

        fields = '__all__'
class DosyaIadeForm(forms.ModelForm):
    class Meta:
        model = DosyaIade
        fields = '__all__'

class DosyaIliskiForm(forms.ModelForm):
    class Meta:
        model = DosyaIliski
        fields = ('Adi')
