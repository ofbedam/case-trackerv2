from django.db import models
from kisiler.models import Kisi
from cocuklar.models import Cocuk
from yerler.models import Country
from kurumlar.models import Kurum
import datetime

from django.core.exceptions import ValidationError
#
# class DosyaBase(models.Model):
#     yil = models.PositiveIntegerField(null=True, blank=True)
#     sayi = models.PositiveIntegerField(null=True, blank=True)
#
#     class Meta:
#         abstract = True
#
# class DosyaCKIade(DosyaBase):
#     pass
#
# class DosyaCKIliski(DosyaBase):
#     def clean(self):
#         existing_entry = DosyaCKIliski.objects.filter(yil=self.yil, sayi=self.sayi).exclude(pk=self.pk).first()
#         if existing_entry:
#             raise ValidationError("Aynı tarih ve sayı değerine sahip bir girdi zaten var.")
#
#         existing_ade = DosyaCKIade.objects.filter(yil=self.yil, sayi=self.sayi).first()
#         if existing_ade:
#             raise ValidationError("Aynı tarih ve sayı değerine sahip bir DosyaCKIade girdisi var.")
#

class NihaiSonucTurleri(models.Model):
    id = models.AutoField(primary_key=True)
    adi = models.TextField()

    def __str__(self):
        return self.adi

    class Meta:

        verbose_name_plural = 'Nihai-Sonuç-Türleri'


class MahkemeRedNedenleri(models.Model):
    id = models.AutoField(primary_key=True)
    adi = models.TextField()

    def __str__(self):
        return self.adi

    class Meta:

        verbose_name_plural = 'Mahkeme Red Nedenleri'


class CocuklaYakinlikTurleri(models.Model):
    id = models.AutoField(primary_key=True)
    adi = models.TextField()

    def __str__(self):
        return self.adi

    class Meta:

        verbose_name_plural = 'Çocukla Yakınlık Türleri'

class CocugaBakimTurleri(models.Model):
    id = models.AutoField(primary_key=True)
    adi = models.TextField()

    def __str__(self):
        return self.adi


    class Meta:

        verbose_name_plural = 'Çocuğa Bakım Türleri'




class Dosya1996(models.Model):

    adi = models.CharField(max_length=50)
    # Diğer alanlar eklenebilir

    def __str__(self):
        return f"Ilişki - {self}"

class Dosya1980Velayet(models.Model):

    adi = models.CharField(max_length=50)
    # Diğer alanlar eklenebilir

    def __str__(self):
        return f"Velayet- {self}"


class DosyaBilgi(models.Model):

    adi = models.CharField(max_length=50)
    # Diğer alanlar eklenebilir

    def __str__(self):
        return f"Bilgi - {self}"