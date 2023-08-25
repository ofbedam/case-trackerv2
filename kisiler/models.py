from django.db import models
from yasaltemsilciler.models import YasalTemsilci

from yerler.models import Country
# Create your models here.



class Kisi(models.Model):
    Adi = models.CharField(max_length=100)
    IkinciAdi = models.CharField(max_length=100, blank=True, null=True)
    Soyadi = models.CharField(max_length=100)
    DogumTarihi = models.DateField(blank=True, null=True)
    Cinsiyet = models.CharField(max_length=10, choices=[('Erkek', 'Erkek'), ('Kız', 'Kız')], blank=True, null=True)
    TelefonNumarasi1 = models.CharField(max_length=20, blank=True, null=True)
    TelefonNumarasi2 = models.CharField(max_length=20, blank=True, null=True)
    Eposta = models.EmailField(max_length=100, blank=True, null=True)
    YasalTemsilci = models.ForeignKey(YasalTemsilci, on_delete=models.CASCADE, verbose_name='Yasal Temsilci', db_column='YasalTemsilciID', related_name='kisiler', blank=True, null=True)
    Notlar = models.TextField(blank=True, null=True)
    Ulkesi = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Ülke Adı', db_column='country_id')

    def __str__(self):
        # return self.Adi + ' ' + self.Soyadi

        full_name = ' '.join(filter(None, [self.Adi, self.IkinciAdi, self.Soyadi]))
        return full_name or "İsimsiz Kişi"

    class Meta:
      #  managed = False
        db_table = 'Kisiler'
        verbose_name = 'Kişi'
        verbose_name_plural = "Kişiler"