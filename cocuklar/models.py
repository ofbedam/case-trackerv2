# cocuklar/models.py
from django.db import models
from kisiler.models import Kisiler
from ulkeler.models import Ulkeler
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
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


 # Method to calculate age
    def calculate_age1(self):
        if self.DogumTarihi:
            today = date.today()
            age1 = today.year - self.DogumTarihi.year - ((today.month, today.day) < (self.DogumTarihi.month, self.DogumTarihi.day))
            return age1
        return None

    # Or use @property decorator to create a property
    @property
    def age2(self):
        if self.DogumTarihi:
            today = date.today()
            age2 = today.year - self.DogumTarihi.year - ((today.month, today.day) < (self.DogumTarihi.month, self.DogumTarihi.day))
            return age2
        return None

        # Method to calculate age in "X years, Y months, Z days" format

    def calculate_age(self):
        if self.DogumTarihi:
            today = date.today()
            age = today.year - self.DogumTarihi.year - (
                        (today.month, today.day) < (self.DogumTarihi.month, self.DogumTarihi.day))

            birth_month = self.DogumTarihi.month
            birth_day = self.DogumTarihi.day

            if today.month < birth_month or (today.month == birth_month and today.day < birth_day):
                age -= 1
                months = (today.month + 12) - birth_month
            else:
                months = today.month - birth_month

            days = today.day - birth_day
            if days < 0:
                months -= 1
                days += 30  # Assuming every month has 30 days for simplicity

            return f"{age} years, {months} months, {days} days"
        return None

        # Method to calculate the date when the Cocuk reaches 16 years old


    def Yas16_Tarih(self):
            if self.DogumTarihi:
                return self.DogumTarihi + relativedelta(years=16)

    def Yas19_Tarih(self):
                if self.DogumTarihi:
                    return self.DogumTarihi + relativedelta(years=19)