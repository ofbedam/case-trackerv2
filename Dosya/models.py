from django.db import models
from kisiler.models import Kisiler
from cocuklar.models import Cocuklar
from yerler.models import Country
from kurumlar.models import Kurumlar
import datetime




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


class Dosya(models.Model):
    @classmethod
    def get_latest_yil_sayi(cls, dosya_kodu):
        latest_dosya = cls.objects.filter(dosya_kodu=dosya_kodu).order_by('-yil', '-sayi').first()
        if latest_dosya:
            return latest_dosya.yil, latest_dosya.sayi
        return None, None
    @classmethod
    def get_latest_dosya_id(cls, dosya_kodu):
        latest_dosya = cls.objects.filter(dosya_kodu=dosya_kodu).order_by('-id').first()
        if latest_dosya:
            return latest_dosya.yil, latest_dosya.sayi
        return None, None
    DOSYA_KODLARI = [
        ('A', 'A- 3-12-1980_IADE'),
        ('B', 'B- 3-12-1980-ILISKI'),
        ('C', 'C- 1996'),
        ('D', 'D- 3-13 (1980-VELAYET)'),
        ('E', 'E- 3-12-Bilgi'),
    ]

    dosya_kodu = models.CharField(
        verbose_name='Dosya Kodu',
        max_length=1,
        choices=DOSYA_KODLARI,
    )


    yil = models.PositiveIntegerField( null=True, blank=True)

    sayi = models.PositiveIntegerField(null=True, blank=True)
    aciklama = models.TextField(null=True, blank=True)
    DosyaAcilisTarihi = models.DateField(verbose_name="Açma Tarihi")
    DosyaDurumu = models.CharField(max_length=10, choices=[('Açık', 'Açık'), ('Kapalı', 'Kapalı'), ('Arşiv', 'Arşiv')], default='Açık')
    DosyaKapatmaTarihi = models.DateField(null=True, blank=True, verbose_name="Kapatma Tarihi")



    # Add ManyToManyField for Cocuklar
    Cocuklar = models.ManyToManyField(Cocuklar, verbose_name='Çocuk Adı', related_name='dosya')




    class Meta:

        verbose_name_plural = 'dosyalar'
        unique_together = ['dosya_kodu', 'yil', 'sayi']  # Kombinasyonun benzersiz olmasını sağlar
        db_table = 'dosya_listesi'



    def __str__(self):
        cocuklar_list = ", ".join([cocuk.__str__() for cocuk in self.Cocuklar.all()])
        return f"Dosya ID: {self.id}, Yil: {self.yil}, Sayı: {self.sayi}, Dosya Tür: {self.dosya_kodu},  Durum: {self.DosyaDurumu}, Cocuklar: {cocuklar_list}"


# çocuk iade dosyası modeli

class DosyaIade(models.Model):
    dosya = models.OneToOneField(Dosya, on_delete=models.CASCADE, primary_key=True)

    GonderenUlke = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Gönderen Ülke')
    YerineGetirenUlke = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Yerine Getiren Ülke',
                                          related_name='yerine_getiren_dosyaiade')
    TalepEdenKurum = models.ForeignKey(Kurumlar, on_delete=models.CASCADE, verbose_name='Talep Eden Kurum',
                                      related_name='talep_eden_kurum_dosyaiade',
                                       null=True, blank=True)
    TalepEdenKurumTarih = models.DateField(null=True, blank=True)
    TalepEdenKurumReferans = models.CharField(max_length=50, blank=True)
    basvurucu = models.ForeignKey(Kisiler, related_name='dosyaiade_basvurucu', on_delete=models.CASCADE,
                                  verbose_name='Başvurucu',  null=True, blank=True)

    BasvurucununCocugaYakinligi = models.ForeignKey(CocuklaYakinlikTurleri, related_name='dosyaiade_basvurucuyakinlik',
                                                          on_delete=models.CASCADE,
                                                          verbose_name='8-a Başvurucunun çocukla yakınlığı', null=True,
                                                          blank=True)
    karsi_taraf = models.ForeignKey(Kisiler, related_name='dosyaiade_karsi_taraf', on_delete=models.CASCADE,
                                    verbose_name='Karşı Taraf',  null=True, blank=True)
    KarsiTarafinCocugaYakinligi = models.ForeignKey(CocuklaYakinlikTurleri, related_name='dosyaiade_karsiyakinlik',
                                                          on_delete=models.CASCADE,
                                                          verbose_name='9-a-Kaçıranın çocukla yakınlığı', null=True,
                                                          blank=True)
    notlar  = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"Iade - {self.dosya}"

    class Meta:

        verbose_name_plural = 'Çocuk İade Dosyaları'

    ######### Talep1980CK DOSYA TÜRÜNE ÖZGÜ ALANLAR  ############





# çocuk iade dosyası modeli sonu


class Dosya1980CK(models.Model):
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















class DosyaIliski(models.Model):
    dosya = models.OneToOneField(Dosya, on_delete=models.CASCADE, primary_key=True)

    # Diğer alanlar eklenebilir

    def __str__(self):
        return f"Ilişki - {self.dosya}"

    class Meta:
        verbose_name_plural = 'Kişisel İlişki Dosyaları'



    GonderenUlke = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Gönderen Ülke')
    YerineGetirenUlke = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Yerine Getiren Ülke',
                                         related_name='yerine_getiren_dosyailiski')
    TalepEdenKurum = models.ForeignKey(Kurumlar, on_delete=models.CASCADE, verbose_name='Talep Eden Kurum',
                                      related_name='talep_eden_kurum_dosyailiski',
                                       null=True, blank=True)
    TalepEdenKurumTarih = models.DateField(null=True, blank=True)
    TalepEdenKurumReferans = models.CharField(max_length=50, blank=True)
    basvurucu = models.ForeignKey(Kisiler, related_name='dosyailiski_basvurucu', on_delete=models.CASCADE,
                                  verbose_name='Başvurucu',  null=True, blank=True)

    BasvurucununCocugaYakinligi = models.ForeignKey(CocuklaYakinlikTurleri, related_name='dosyailiski_basvurucuyakinlik',
                                                          on_delete=models.CASCADE,
                                                          verbose_name='8-a Başvurucunun çocukla yakınlığı', null=True,
                                                          blank=True)
    karsi_taraf = models.ForeignKey(Kisiler, related_name='dosyailiski_karsi_taraf', on_delete=models.CASCADE,
                                    verbose_name='Karşı Taraf',  null=True, blank=True)
    KarsiTarafinCocugaYakinligi = models.ForeignKey(CocuklaYakinlikTurleri, related_name='dosyailiski_karsiyakinlik',
                                                          on_delete=models.CASCADE,
                                                          verbose_name='9-a-Kaçıranın çocukla yakınlığı', null=True,
                                                          blank=True)

    notlar = models.TextField(null=True, blank=True)












class Dosya1996(models.Model):
    dosya = models.OneToOneField(Dosya, on_delete=models.CASCADE, primary_key=True)
    adi = models.CharField(max_length=50)
    # Diğer alanlar eklenebilir

    def __str__(self):
        return f"Ilişki - {self.dosya}"

class Dosya1980Velayet(models.Model):
    dosya = models.OneToOneField(Dosya, on_delete=models.CASCADE, primary_key=True)
    adi = models.CharField(max_length=50)
    # Diğer alanlar eklenebilir

    def __str__(self):
        return f"Ilişki - {self.dosya}"


class DosyaBilgi(models.Model):
    dosya = models.OneToOneField(Dosya, on_delete=models.CASCADE, primary_key=True)
    adi = models.CharField(max_length=50)
    # Diğer alanlar eklenebilir

    def __str__(self):
        return f"Ilişki - {self.dosya}"