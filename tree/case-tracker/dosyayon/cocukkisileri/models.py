from django.db import models


from kisiler.models import Kisiler
from cocuklar.models import Cocuklar
# Create your models here.

class CocukKisileri(models.Model):
    CocukKisiID = models.AutoField(primary_key=True)
    CocukID = models.ForeignKey(Cocuklar, on_delete=models.CASCADE, verbose_name='Çocuk Adı', db_column='CocukID', related_name='cocuk_kisileri')
    KisiID = models.ForeignKey(Kisiler, on_delete=models.CASCADE, verbose_name='Adı', db_column='KisiID', related_name='cocuk_kisileri')
    Yakinlik = models.CharField(max_length=20,
                                choices=[('Anne', 'Anne'), ('Baba', 'Baba'), ('Yakın Akraba', 'Yakın Akraba'),
                                         ('Kurum', 'Kurum'), ('Vasi', 'Vasi')])

    def __str__(self):
        return f"CocukKisiID: {self.CocukKisiID}, CocukID: {self.CocukID}, KisiID: {self.KisiID}, Yakinlik: {self.Yakinlik}"

    class Meta:
     #   managed = False
        db_table = 'CocukKisileri'
