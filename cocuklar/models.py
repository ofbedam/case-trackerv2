# cocuklar/models.py
from django.db import models
from kisiler.models import Kisiler
from ulkeler.models import Ulkeler
class Cocuklar(models.Model):
    CocukID = models.AutoField(primary_key=True)
    Adi = models.CharField(max_length=100)
    IkinciAdi = models.CharField(max_length=100, blank=True, null=True)
    Soyadi = models.CharField(max_length=100)
    DogumTarihi = models.DateField(blank=True, null=True)
    Cinsiyet = models.CharField(max_length=10, choices=[('Erkek', 'Erkek'), ('Kız', 'Kız')], blank=True, null=True)

    AnneAdi = models.ForeignKey(Kisiler, related_name='annesi', on_delete=models.CASCADE,
                                    verbose_name='Annesinin Adı', db_column='AnneAdi', null=True, blank=True)


    BabaAdi = models.ForeignKey(Kisiler, on_delete=models.CASCADE, related_name='babasi', null=True, blank=True)

    IletisimBilgileri = models.TextField(blank=True, null=True)
    Notlar = models.TextField(blank=True, null=True)
    UlkesiID = models.ForeignKey(Ulkeler, on_delete=models.CASCADE, verbose_name='Ülke Adı', db_column='UlkesiID', related_name='cocuklar')
    # Add ManyToManyField for Dosyalar
    #dosyalar = models.ManyToManyField('Dosyalar', verbose_name='Çocuğa İlişkin Dosyalar', related_name='cocuklar')

    def __str__(self):
        return f"{self.Adi} {self.Soyadi}"

    class Meta:
        db_table = 'Cocuklar'


