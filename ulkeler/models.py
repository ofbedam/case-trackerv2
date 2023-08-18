from django.db import models

# Create your models here.
class Ulkeler(models.Model):
    UlkeID = models.AutoField(primary_key=True)
    UlkeAdi = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.UlkeAdi

    class Meta:
       # managed = False
        db_table = 'Ulkeler'

        verbose_name_plural = "Ülkeler"

