#kurumlar/models.py
from django.db import models
from yerler.models import Country, City, State




# Create your models here.

class SehirIlce(models.Model):
    ID = models.AutoField(primary_key=True)
    Adi = models.CharField(max_length=50, blank=False)


    def __str__(self):
        return self.Adi

    class Meta:
        managed = True
        db_table = 'SehirIlce'
class KurumTurleri(models.Model):
    TurID = models.AutoField(primary_key=True)
    TurAdi = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.TurAdi

    class Meta:
        managed = True
        db_table = 'KurumTurleri'
class Kurumlar(models.Model):
    KurumID = models.AutoField(primary_key=True)
    UlkeID = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Ülkesi',
                           db_column='Countryid', related_name='ulkesi', default='1')

    State = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name='Şehir',
                           db_column='Stateid', related_name='sehri', default='1')


    City = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İlçe',
                            db_column='Cityid', related_name='ilcesi', default='Default City')

    KurumTuru = models.ForeignKey(KurumTurleri, on_delete=models.CASCADE, verbose_name='Türü',
                              db_column='TurID', related_name='kurum')

    KurumSiraNo = models.CharField(max_length=20, blank=True)
    KurumAdi = models.CharField(max_length=20, blank=True)
    Adresi = models.CharField(max_length=200, blank=True)
    Telefon1 = models.CharField(max_length=20, blank=True)
    Telefon2 = models.CharField(max_length=20, blank=True)
    Email = models.CharField(max_length=40, blank=True)
    IletisimKisisi = models.CharField(max_length=50, blank=True)




    def __str__(self):
        return f"{self.KurumID}, {self.KurumAdi}, {self.KurumSiraNo}, {self.KurumTuru}, {self.State}, , {self.UlkeID}"

    # def __str__(self):
    #     return f"{self.KurumAdi} {self.KurumSıraNo} {self.KurumTuru} {self.SehirIlcesi}"

    class Meta:
       # managed = False
        db_table = 'Kurumlar'