#dosyalar/models.py


from django.db import models

from ulkeler.models import Ulkeler
from kisiler.models import Kisiler
from cocuklar.models import Cocuklar
from yerler.models import Country
from kurumlar.models import Kurumlar

# Create your models here.

#### DOSYA ZORUNLU ORTAK ALANLAR BAŞLANGICI
class Dosyalar(models.Model):
    DosyaID = models.AutoField(primary_key=True)
    DosyaKodu = models.CharField(verbose_name='Dosya Kodu', max_length=20,
                                 choices=[('3-12', '3-12 (1980CK&1996Sözleşme)'), ('3-13', '3-13 (1980Velayet)'),('3-12-Bilgi', '3-12-Bilgi')])
    DosyaYil = models.PositiveIntegerField()
    DosyaNo = models.PositiveIntegerField()


    Aciklama = models.TextField(null=True, blank=True)
    DosyaAcilisTarihi = models.DateField()
    TalepEdenKurum = models.ForeignKey(Kurumlar, on_delete=models.CASCADE, verbose_name='Talep Eden Kurum',
                                       db_column='talepeden_kurumid', related_name='talep_eden_kurum_dosyalar',
                                       null=True, blank=True)
    TalepEdenKurumTarih = models.DateField(null=True, blank=True)
    TalepEdenKurumReferans = models.CharField(max_length=50, blank=True)

    DosyaKapatmaTarihi = models.DateField(null=True, blank=True)
    DosyaDurumu = models.CharField(max_length=10, choices=[('Açık', 'Açık'), ('Kapalı', 'Kapalı'), ('Arşiv', 'Arşiv')])


#### DOSYA ORTAK ALANLAR SONU




    DosyaTuru = models.CharField(verbose_name='Tür', max_length=20,
                                 choices=[('1980CK_iade', '1980 ÇK İade'),
                                          ('1980CK_sahsi_iliski', '1980 ÇK Şahsi İlişki'), ('1996', '1996')])

    GonderenUlke = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Gönderen Ülke',
                                       db_column='gonderen_country_id', related_name='gonderen_dosyalar')
    YerineGetirenUlke = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Yerine Getiren Ülke',
                                            db_column='yerinegetiren_country_id', related_name='yerine_getiren_dosyalar')

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

######### Talep1980CK DOSYA TÜRÜNE ÖZGÜ ALANLAR  ############
class NihaiSonucTurleri(models.Model):
    id = models.AutoField(primary_key=True)
    adi = models.TextField()

    def __str__(self):
        return self.adi

    class Meta:
       # managed = False
        db_table = 'NihaiSonucTurleri'


class MahkemeRedNedenleri(models.Model):
    id = models.AutoField(primary_key=True)
    adi = models.TextField()

    def __str__(self):
        return self.adi

    class Meta:
        # managed = False
        db_table = 'MahkemeRedNedenleri'



class CocuklaYakinlikTurleri(models.Model):
    id = models.AutoField(primary_key=True)
    adi = models.TextField()

    def __str__(self):
        return self.adi

    class Meta:
        # managed = False
        db_table = 'CocuklaYakinlikTurleri'

class CocugaBakimTurleri(models.Model):
    id = models.AutoField(primary_key=True)
    adi = models.TextField()

    def __str__(self):
        return self.adi

    class Meta:
        # managed = False
        db_table = 'CocugaBakimTurleri'


class Talep1980CK(models.Model):
    nihai_sonuc_4a = models.ForeignKey(NihaiSonucTurleri, related_name='nihaisonuc', on_delete=models.CASCADE,
                                       verbose_name='4-a Nihai Sonuç', null=True, blank=True)

    arabuluculuk_basvuru_4b = models.CharField(verbose_name='4-b-Taraflar arabuluculuk başvurdu mu', max_length=20,
                                               null=True,
                                               blank=True,
                                               choices=[('Evet', 'Evet'), ('Hayır', 'Hayır'),
                                                        ('Bilinmiyor', 'Bilinmiyor')])

    gecici_kisisel_iliski_4c = models.CharField(
        verbose_name='4-c- Geçici kişiel ilişki emredildi mi veya kararlaştırıldı mı?', max_length=20,
        null=True, blank=True,
        choices=[('Evet', 'Evet'), ('Hayır', 'Hayır'), ('Bilinmiyor', 'Bilinmiyor')])

    mahkeme_red_neden_5 = models.ForeignKey(MahkemeRedNedenleri, related_name='nihaisonuc', on_delete=models.CASCADE,
                                            verbose_name='5-Mahkeme Red Nedeni', null=True, blank=True)

    basvurunun_alindigi_tarih_6a = models.DateField(verbose_name='6-a-Başvurunun Alındığı Tarih', null=True, blank=True)
    nihai_sonuc_tarihi_6c = models.DateField(verbose_name='6-c-Nihai Sonuç Tarihi', null=True, blank=True)

    karar_anlasma_yerine_6d = models.CharField(verbose_name='6-d-Karar yada anlaşma yerine getirildi mi??',
                                               max_length=20, choices=[('Evet', 'Evet'), ('Hayır', 'Hayır'),
                                                                       ('Bilinmiyor', 'Bilinmiyor')])

    karar_anlasma_yerine_6e = models.DateField(verbose_name='6-e-Karar yada anlaşma yerine getirildiği tarih',
                                               null=True, blank=True)

    mahkeme_karari_temyiz_edildi_mi = models.CharField(verbose_name='7-a-Mahkeme kararı temyiz edildi mi',
                                                       max_length=20, choices=[('Evet', 'Evet'), ('Hayır', 'Hayır'),
                                                                               ('Evet - 1 Seviye', 'Evet - 1 Seviye'),
                                                                               ('Evet -2 Seviye', 'Evet -2 Seviye'),
                                                                               ('Evet -3 Seviye', 'Evet -3 Seviye'),
                                                                               ('Bilinmiyor', 'Bilinmiyor')])



    evet_ise_ilk_derece_mahkemesinde_davanin_sonucu_7b = models.CharField(
        verbose_name='7-b- Evet ise, ilk derece mahkemesinde davanın sonucu ne oldu?', max_length=40, null=True,
        blank=True,
        choices=[('Nihai temyizdeki sonuçla aynı', 'Nihai temyizdeki sonuçla aynı'),
                 ('Nihai temyizdeki sonuçtan farklı', 'Nihai temyizdeki sonuçtan farklı'),
                 ('Bilinmiyor', 'Bilinmiyor')])

    ikinci_derece_mahkemenin_karar_tarihi_7d = models.DateField(
        verbose_name='7-d-İkinci derece mahkemenin karar tarihi', null=True, blank=True)

    ucuncu_derece_mahkemenin_karar_tarihi_7e = models.DateField(
        verbose_name='7-e-Üçüncü derece mahkemenin karar tarihi', null=True, blank=True)

    basvurucunun_cocukla_yakinligi_8a = models.ForeignKey(CocuklaYakinlikTurleri,
                                                          related_name='Başvurucunun_çocukla_yakınlığı',
                                                          on_delete=models.CASCADE,
                                                          verbose_name='8-a-Başvurucunun çocukla yakınlığı', null=True,
                                                          blank=True)

    basvurucunun_bakim_durumu_8b = models.ForeignKey(CocugaBakimTurleri,
                                                     related_name='basvurucunun_cocuga_bakimi',
                                                     on_delete=models.CASCADE,
                                                     verbose_name=' 8-b-Başvurucunun çocuğa bakım durumu', null=True,
                                                     blank=True)

    kaciranin_cocukla_yakinligi_9a = models.ForeignKey(CocuklaYakinlikTurleri,
                                                       related_name='kaciranin_cocukla_yakinligi',
                                                       on_delete=models.CASCADE,
                                                       verbose_name='9-a-Kaçıranın çocukla yakınlığı', null=True,
                                                       blank=True)

    kaciranin_bakim_durumu_9b = models.ForeignKey(CocugaBakimTurleri,
                                                  related_name='kaciranin_cocuga_bakimi',
                                                  on_delete=models.CASCADE,
                                                  verbose_name=' 9-b-Kaçıranın çocuğa bakım durumu', null=True,
                                                  blank=True)

    diger_aciklamalar_11 = models.CharField(verbose_name='11-Diğer Açıklamalar?', max_length=200, null=True,
                                            blank=True)


######### Talep1980CK DOSYA TÜRÜNE ÖZGÜ ALANLAR SONU  ############