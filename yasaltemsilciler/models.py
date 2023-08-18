from django.db import models

# Create your models here.
from yerler.models import Country
class YasalTemsilciler(models.Model):
    TemsilciID = models.AutoField(primary_key=True)
    Unvani = models.CharField(max_length=100)
    Adi = models.CharField(max_length=100)
    IkinciAdi = models.CharField(max_length=100, blank=True, null=True)
    Soyadi = models.CharField(max_length=100)
    DogumTarihi = models.DateField(blank=True, null=True)
    Cinsiyet = models.CharField(max_length=10, choices=[('Erkek', 'Erkek'), ('Kız', 'Kız')], blank=True, null=True)
    TelefonNumarasi1 = models.CharField(max_length=20, blank=True, null=True)
    TelefonNumarasi2 = models.CharField(max_length=20, blank=True, null=True)
    Eposta = models.EmailField(max_length=100, blank=True, null=True)
    Notlar = models.TextField(blank=True, null=True)
    UlkesiID = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Ülke Adı', db_column='country_id', related_name='yasal_temsilciler')

    def __str__(self):
        return self.Adi + ' ' + self.Soyadi

    class Meta:
      #  managed = False
        db_table = 'YasalTemsilciler'
        verbose_name_plural = "Yasal Temsilciler"
