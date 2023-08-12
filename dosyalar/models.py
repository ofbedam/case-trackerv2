from django.db import models

from ulkeler.models import Ulkeler
from kisiler.models import Kisiler
from cocuklar.models import Cocuklar
from yerler.models import Country

# Create your models here.


class Dosyalar(models.Model):
    DosyaID = models.AutoField(primary_key=True)
    DosyaYil = models.IntegerField()
    DosyaNo = models.IntegerField()
    Aciklama = models.TextField()
    DosyaTuru = models.CharField(verbose_name='Tür', max_length=20,
                                 choices=[('1980 ÇK', '1980 ÇK'), ('1996', '1996'), ('1980 Velayet', '1980 Velayet'),
                                          ('Bilgi', 'Bilgi')])
    DosyaAcilisTarihi = models.DateField()
    DosyaKapatmaTarihi = models.DateField(null=True, blank=True)
    DosyaDurumu = models.CharField(max_length=10, choices=[('Açık', 'Açık'), ('Kapalı', 'Kapalı'), ('Arşiv', 'Arşiv')])
    GonderenUlke = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Gönderen Ülke',
                                       db_column='gonderen_country_id', related_name='gonderen_dosyalar')
    YerineGetirenUlke = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Yerine Getiren Ülke',
                                            db_column='yerinegetiren_country_id', related_name='yerine_getiren_dosyalar')
    TalepEdenKurumTarih = models.DateField(null=True, blank=True)
    TalepEdenKurumReferans = models.CharField(max_length=50, blank=True)
    basvurucu = models.ForeignKey(Kisiler, related_name='dosyalar_basvurucu', on_delete=models.CASCADE,
                                  verbose_name='Başvurucu', db_column='basvurucu_id', null=True, blank=True)

    BasvurucununCocugaYakinliği = models.CharField(null=True, blank=True, max_length=20, choices=[('Anne', 'Anne'), ('Baba', 'Baba'),
                                                                           ('Büyükanne/baba', 'Büyükanne/baba'),
                                                                           ('Diğer Akraba', 'Diğer Akraba'),
                                                                           ('Vasi', 'Vasi'), ('Kurum', 'Kurum'),
                                                                           ('Diğer', 'Diğer'), ])
    karsi_taraf = models.ForeignKey(Kisiler, related_name='dosyalar_karsi_taraf', on_delete=models.CASCADE,
                                    verbose_name='Karşı Taraf', db_column='karsi_taraf_id', null=True, blank=True)
    KarsiTarafinCocugaYakinliği = models.CharField(null=True, blank=True,max_length=20, choices=[('Anne', 'Anne'), ('Baba', 'Baba'),
                                                                           ('Büyükanne/baba', 'Büyükanne/baba'),
                                                                           ('Diğer Akraba', 'Diğer Akraba'),
                                                                           ('Vasi', 'Vasi'), ('Kurum', 'Kurum'),
                                                                           ('Diğer', 'Diğer'), ])



    # Add ManyToManyField for Cocuklar
    Cocuklar = models.ManyToManyField(Cocuklar, verbose_name='Çocuk Adı', related_name='dosyalar')

    def __str__(self):
        cocuklar_list = ", ".join([cocuk.__str__() for cocuk in self.Cocuklar.all()])
        return f"DosyaID: {self.DosyaID}, DosyaYil: {self.DosyaYil}, DosyaNo: {self.DosyaNo}, DosyaTür: {self.DosyaTuru},  Durum: {self.DosyaDurumu},Cocuklar: {cocuklar_list}"

    class Meta:
        unique_together = [['DosyaYil', 'DosyaNo']]
        db_table = 'Dosyalar'

    def save(self, *args, **kwargs):
        if not self.DosyaID:
            # Check if there are existing records with the same DosyaYil
            existing_records = Dosyalar.objects.filter(DosyaYil=self.DosyaYil)
            if existing_records.exists():
                # Get the maximum DosyaNo for the same DosyaYil and increment it by 1
                max_dosya_no = existing_records.aggregate(models.Max('DosyaNo'))['DosyaNo__max']
                self.DosyaNo = max_dosya_no + 1
            else:
                # If no existing records with the same DosyaYil, set DosyaNo to 1
                self.DosyaNo = 1

        super(Dosyalar, self).save(*args, **kwargs)

# class Dosyalar(models.Model):
#     DosyaID = models.AutoField(primary_key=True)
#     DosyaYil = models.IntegerField()
#     DosyaNo = models.IntegerField()
#     Aciklama = models.TextField()
#     DosyaTuru = models.CharField(max_length=20, choices=[('1980 ÇK', '1980 ÇK'), ('1996', '1996'), ('1980 Velayet', '1980 Velayet'), ('Bilgi', 'Bilgi')])
#     DosyaAcilisTarihi = models.DateField()
#     DosyaKapatmaTarihi = models.DateField(null=True, blank=True)
#     DosyaDurumu = models.CharField(max_length=10, choices=[('Açık', 'Açık'), ('Kapalı', 'Kapalı'), ('Arşiv', 'Arşiv')])
#     GonderenUlkeID = models.ForeignKey(Ulkeler, on_delete=models.CASCADE, verbose_name='Gönderen Ülke', db_column='GonderenUlkeID', related_name='gonderen_dosyalar')
#     YerineGetirenUlkeID = models.ForeignKey(Ulkeler, on_delete=models.CASCADE, verbose_name='Yerine Getiren Ülke', db_column='YerineGetirenUlkeID', related_name='yerine_getiren_dosyalar')
#     TalepEdenKurumTarih = models.DateField(null=True, blank=True)
#     TalepEdenKurumReferans = models.CharField(max_length=50, blank=True)
#     CocukID = models.ForeignKey(Cocuklar, on_delete=models.CASCADE, verbose_name='Çocuk Adı', db_column='CocukID', related_name='dosyalar')
#
#     def __str__(self):
#         return f"ID: {self.DosyaID}, DosyaYil/No: {self.DosyaYil}, / {self.DosyaNo}, Aciklama: {self.Aciklama}, DosyaTuru: {self.DosyaTuru}, AcilisTarihi: {self.DosyaAcilisTarihi}, KapatmaTarihi: {self.DosyaKapatmaTarihi}, DosyaDurumu: {self.DosyaDurumu}, GonderenUlke: {self.GonderenUlkeID}, YerineGetirenUlke: {self.YerineGetirenUlkeID}, TalepEdenKurumTarih: {self.TalepEdenKurumTarih}, TalepEdenKurumReferans: {self.TalepEdenKurumReferans}, CocukID: {self.CocukID}"
#
#     class Meta:
#            managed = False
#         db_table = 'Dosyalar'
#
