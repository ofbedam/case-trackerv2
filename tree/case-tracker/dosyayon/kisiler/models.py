from django.db import models
from yasaltemsilciler.models import YasalTemsilciler
from ulkeler.models import Ulkeler
from yerler.models import Country
# Create your models here.



class Kisiler(models.Model):
    KisiID = models.AutoField(primary_key=True)
    Adi = models.CharField(max_length=100)
    IkinciAdi = models.CharField(max_length=100, blank=True, null=True)
    Soyadi = models.CharField(max_length=100)
    DogumTarihi = models.DateField(blank=True, null=True)
    Cinsiyet = models.CharField(max_length=10, choices=[('Erkek', 'Erkek'), ('Kız', 'Kız')], blank=True, null=True)
    TelefonNumarasi1 = models.CharField(max_length=20, blank=True, null=True)
    TelefonNumarasi2 = models.CharField(max_length=20, blank=True, null=True)
    Eposta = models.EmailField(max_length=100, blank=True, null=True)
    YasalTemsilciID = models.ForeignKey(YasalTemsilciler, on_delete=models.CASCADE, verbose_name='Yasal Temsilci', db_column='YasalTemsilciID', related_name='kisiler', blank=True, null=True)
    Notlar = models.TextField(blank=True, null=True)
    UlkesiID = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Ülke Adı', db_column='UlkesiID')

    def __str__(self):
        return self.Adi + ' ' + self.Soyadi

    class Meta:
      #  managed = False
        db_table = 'Kisiler'