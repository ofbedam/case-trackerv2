from django.db import models
from kisiler.models import Kisi
from cocuklar.models import Cocuk
from yerler.models import Country
from kurumlar.models import Kurum
from dosya2.models import CocuklaYakinlikTurleri, NihaiSonucTurleri, MahkemeRedNedenleri, CocugaBakimTurleri
import datetime

from django.core.exceptions import ValidationError



class DosyaCKIliski(models.Model):
    yil = models.PositiveIntegerField(null=True, blank=True)
    sayi = models.PositiveIntegerField(null=True, blank=True)
    aciklama = models.TextField(null=True, blank=True)
    DosyaAcilisTarihi = models.DateField(verbose_name="Açma Tarihi")
    DosyaDurumu = models.CharField(max_length=10, choices=[('Açık', 'Açık'), ('Kapalı', 'Kapalı'), ('Arşiv', 'Arşiv')],
                                   default='Açık')
    DosyaKapatmaTarihi = models.DateField(null=True, blank=True, verbose_name="Kapatma Tarihi")

    GonderenUlke = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Gönderen Ülke',
                                     related_name='gonderenulke_dosya2iliski')
    YerineGetirenUlke = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Yerine Getiren Ülke',
                                          related_name='yerine_getiren_dosya2iliski')
    TalepEdenKurum = models.ForeignKey(Kurum, on_delete=models.CASCADE, verbose_name='Talep Eden Kurum',
                                       related_name='talep_eden_kurum_dosya2iliski',
                                       null=True, blank=True)
    TalepEdenKurumTarih = models.DateField(null=True, blank=True)
    TalepEdenKurumReferans = models.CharField(max_length=50, blank=True)

    # Add ManyToManyField for Cocuklar
    Cocuklar = models.ManyToManyField(Cocuk, verbose_name='Çocuk Adı', related_name='cocuk_dosya2iliski')

    basvurucu = models.ForeignKey(Kisi, related_name='dosya2iliski_basvurucu', on_delete=models.CASCADE,
                                  verbose_name='Başvurucu', null=True, blank=True)

    BasvurucununCocugaYakinligi = models.ForeignKey(CocuklaYakinlikTurleri, related_name='dosya2iliski_basvurucuyakinlik',
                                                    on_delete=models.CASCADE,
                                                    verbose_name='8-a Başvurucunun çocukla yakınlığı', null=True,
                                                    blank=True)
    karsi_taraf = models.ForeignKey(Kisi, related_name='dosya2iliski_karsi_taraf', on_delete=models.CASCADE,
                                    verbose_name='Karşı Taraf', null=True, blank=True)
    KarsiTarafinCocugaYakinligi = models.ForeignKey(CocuklaYakinlikTurleri, related_name='dosya2iliski_karsiyakinlik',
                                                    on_delete=models.CASCADE,
                                                    verbose_name='9-a-Kaçıranın çocukla yakınlığı', null=True,
                                                    blank=True)
    notlar = models.TextField(null=True, blank=True)

    nihai_sonuc_4a = models.ForeignKey(NihaiSonucTurleri, related_name='nihaisonuc_dosya2iliski', on_delete=models.CASCADE,
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

    mahkeme_red_neden_5 = models.ForeignKey(MahkemeRedNedenleri, related_name='mahkemereden_dosya2iliski', on_delete=models.CASCADE,
                                            verbose_name='5-Mahkeme Red Nedeni', null=True, blank=True)

    basvurunun_alindigi_tarih_6a = models.DateField(verbose_name='6-a-Başvurunun Alındığı Tarih', null=True, blank=True)
    nihai_sonuc_tarihi_6c = models.DateField(verbose_name='6-c-Nihai Sonuç Tarihi', null=True, blank=True)

    karar_anlasma_yerine_6d = models.CharField(null=True, blank=True, verbose_name='6-d-Karar yada anlaşma yerine getirildi mi??',
                                               max_length=20, choices=[('Evet', 'Evet'), ('Hayır', 'Hayır'),
                                                                       ('Bilinmiyor', 'Bilinmiyor')])

    karar_anlasma_yerine_6e = models.DateField(verbose_name='6-e-Karar yada anlaşma yerine getirildiği tarih',
                                               null=True, blank=True)

    mahkeme_karari_temyiz_edildi_mi = models.CharField(null=True, blank=True, verbose_name='7-a-Mahkeme kararı temyiz edildi mi',
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
                                                          related_name='basvurucunun_cocukla_yakinligi_dosya2iliski',
                                                          on_delete=models.CASCADE,
                                                          verbose_name='8-a-Başvurucunun çocukla yakınlığı', null=True,
                                                          blank=True)

    basvurucunun_bakim_durumu_8b = models.ForeignKey(CocugaBakimTurleri,
                                                     related_name='basvurucunun_cocuga_bakimi_dosya2iliski',
                                                     on_delete=models.CASCADE,
                                                     verbose_name=' 8-b-Başvurucunun çocuğa bakım durumu', null=True,
                                                     blank=True)

    kaciranin_cocukla_yakinligi_9a = models.ForeignKey(CocuklaYakinlikTurleri,
                                                       related_name='kaciranin_cocukla_yakinligi_dosya2iliski',
                                                       on_delete=models.CASCADE,
                                                       verbose_name='9-a-Kaçıranın çocukla yakınlığı', null=True,
                                                       blank=True)

    kaciranin_bakim_durumu_9b = models.ForeignKey(CocugaBakimTurleri,
                                                  related_name='kaciranin_cocuga_bakimi_dosya2iliski',
                                                  on_delete=models.CASCADE,
                                                  verbose_name=' 9-b-Kaçıranın çocuğa bakım durumu', null=True,
                                                  blank=True)

    diger_aciklamalar_11 = models.CharField(verbose_name='11-Diğer Açıklamalar?', max_length=200, null=True,
                                            blank=True)

    def __str__(self):
        return f"Çocukla İlişki - {self.DosyaCKIliski}"

    class Meta:

        verbose_name_plural = 'Çocukla Kişisel İlişki'
        unique_together = ['yil', 'sayi']  # Kombinasyonun benzersiz olmasını sağlar

    def __str__(self):
        cocuklar_list = ", ".join([cocuk.__str__() for cocuk in self.Cocuklar.all()])
        return f"Dosya ID: {self.id}, Yil: {self.yil}, Sayı: {self.sayi},  Durum: {self.DosyaDurumu}, Cocuklar: {cocuklar_list}"

