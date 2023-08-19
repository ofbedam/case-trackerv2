# dosyayon/signals.py
from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from random import randint
from kurumlar.models import KurumTurleri, Kurumlar
from Dosya.models import CocuklaYakinlikTurleri, CocugaBakimTurleri, NihaiSonucTurleri, MahkemeRedNedenleri
from yerler.models import Country, State, City
from cocuklar.models import Cocuklar
from kisiler.models import Kisiler

import random
from datetime import date, timedelta
from Dosya.models import Dosya
# dosyayon/signals.py
from django.db.models.signals import pre_migrate
from django.dispatch import receiver
from django.apps import apps
from django.db import connection
import os


import os
from django.db import connection
from django.dispatch import receiver



import random
from datetime import date, timedelta
from django.db.models.signals import post_migrate
from django.dispatch import receiver



NAMES_NEW = [
    "Eleanor", "Sebastian", "Aria", "Felix", "Lila", "Victor", "Zara", "Theodore", "Amara", "Adrian",
    "Luna", "Ezra", "Athena", "Maximus", "Evelyn", "Roman", "Elara", "August", "Cora", "Atticus",
    "Yusuf", "Azra", "Kuzey", "Elif", "Miray", "Aras", "Defne", "Can", "Aylin", "Emir",
    "Lucia", "Matias", "Sofía", "Leonardo", "Valentina", "Santiago", "Isabella", "Dante", "Emma", "Mariana"
]



SURNAMES_NEW = [
    "Çalışkan", "Kara", "Yıldırım", "Aydın", "Başar", "Kaplan", "Demirci", "Altın", "Şahin", "Karaelmas",
    "Oktay", "Ergin", "Kıvanç", "Kocaman", "Kurtuluş", "Ergün", "Şensoy", "Yılmaz", "Can", "Köse",
    "Öztürk", "Karakaş", "Tekin", "Açıkgöz", "Gündüz", "Köksal", "Özen", "Akça", "Durmaz", "Göksel",
    "Aktaş", "Kapıcı", "Sarı", "Kaya", "Demir", "Çelik", "Aydın", "Şahin", "Aksoy", "Ergin",
    "Johnson", "Martinez", "Lee", "Garcia", "Zhang", "Silva", "Walker", "Nguyen", "Lopez", "Andersen",
    "Kaya", "Hansen", "Yılmaz", "Schmidt", "Gonzalez", "Sullivan", "Sato", "Ivanov", "Tan", "Ali",
    "O'Connor", "Sakamoto", "Smith", "Takahashi", "Wilson", "Santos", "Wang", "Peterson", "Arslan", "Fernandez",
    "Chen", "Larsen", "Koc", "Günay", "Miller", "Erdogan", "Wu", "Alves", "Yamamoto", "Kılıç"
]



@receiver(post_migrate)
def create_initial_cocuklar(sender, **kwargs):
    if sender.name != 'cocuklar':  # Replace 'your_app_name' with your actual app name
        return

    for _ in range(20):
        cocuk = Cocuklar.objects.create(
            Adi=f"Test {random.choice(NAMES_NEW)}",
            IkinciAdi=f"{random.choice(NAMES_NEW)}",
            Soyadi=random.choice(SURNAMES_NEW),
            DogumTarihi=date.today() - timedelta(days=random.randint(300, 7000)),
            Cinsiyet=random.choice(['Erkek', 'Kız']),
            Ulkesi=Country.objects.get(pk=randint(1, 230)),
        )
        cocuk.save()



DOSYA_KODLARI = [
    ('A', 'A- 3-12-1980_IADE'),
    ('B', 'B- 3-12-1980-ILISKI'),
    ('C', 'C- 1996'),
    ('D', 'D- 3-13 (1980-VELAYET)'),
    ('E', 'E- 3-12-Bilgi'),
]
DOSYA_KODLARI = [
    ('A', 'A- 3-12-1980_IADE'),
    ('B', 'B- 3-12-1980-ILISKI'),
    ('C', 'C- 1996'),
    ('D', 'D- 3-13 (1980-VELAYET)'),
    ('E', 'E- 3-12-Bilgi'),
]

@receiver(post_migrate)
def create_random_dosyalar(sender, **kwargs):
    if sender.name != 'Dosya':  # Replace 'your_app_name' with your actual app name
        return

    for _ in range(100):
        dosya_kodu = random.choice(DOSYA_KODLARI)
        yil = random.randint(2020, 2023)
        sayi = random.randint(10999, 20000)
        aciklama = f"Rastgele açıklama {_}"
        dosya_acilis_tarihi = date.today() - timedelta(days=random.randint(100, 1000))
        dosya_durumu = random.choice(['Açık', 'Kapalı', 'Arşiv'])
        dosya_kapanis_tarihi = None

        # if dosya_durumu == 'Kapalı':
        #     dosya_kapanis_tarihi = date.today() - timedelta(days=random.randint(365, 700))
        #

        if dosya_durumu == 'Kapalı':
            dosya_kapanis_tarihi = dosya_acilis_tarihi + timedelta(days=random.randint(1, (date.today() - dosya_acilis_tarihi).days - 1))

        dosya = Dosya.objects.create(
            dosya_kodu=dosya_kodu[0],
            yil=yil,
            sayi=sayi,
            aciklama=aciklama,
            DosyaAcilisTarihi=dosya_acilis_tarihi,
            DosyaDurumu=dosya_durumu,
            DosyaKapatmaTarihi=dosya_kapanis_tarihi
        )

        dosya.Cocuklar.set(random.sample(list(Cocuklar.objects.all()), random.randint(1, 15)))  # Assuming you have a Cocuklar queryset

        dosya.save()

@receiver(post_migrate)
def create_initial_kisiler(sender, **kwargs):
    if sender.name != 'kisiler':  # Replace 'your_app_name' with your actual app name
        return

    for _ in range(20):
        kisi = Kisiler.objects.create(
            Adi=f"Test {random.choice(NAMES_NEW)}",
            IkinciAdi=f"{random.choice(NAMES_NEW)}",
            Soyadi=random.choice(SURNAMES_NEW),
            DogumTarihi=date.today() - timedelta(days=random.randint(9125, 20175)),
            Cinsiyet=random.choice(['Erkek', 'Kız']),
            Ulkesi=Country.objects.get(pk=randint(1, 230)),
        )
        kisi.save()


KURUM_LIST = [
    "Ankara 1. Asliye Hukuk Mahkemesi ", "Ankara Cumhuriyet Başsavcılığı", "Aile Bakanlığı", "Dışişliği Bakanlığı", "Almanya Merkezi Makamı"
]


@receiver(post_migrate)
def create_initial_kurumlar(sender, **kwargs):
    if sender.name != 'kurumlar':  # Replace 'your_app_name' with your actual app name
        return

    for _ in range(5):
        kurum = Kurumlar.objects.create(
            KurumAdi =f"Test {random.choice(KURUM_LIST)}",
            KurumTuru = KurumTurleri.objects.first(),  # Assuming you have a Country object to associate
            State = State.objects.first(),  # Assuming you have a Country object to associate
            City =City.objects.first(),  # Assuming you have a Country object to associate
            Country=Country.objects.first(),  # Assuming you have a Country object to associate
        )
        kurum.save()

@receiver(pre_migrate)
def import_initial_data(sender, **kwargs):
    """
    Import initial data from a MySQL dump file during the initial migrations.
    """
    if sender.label in ('yerler'):
        dump_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'initial_data\countries-states-cities-Turkish-2023-8-19.sql')
        with open(dump_file_path, 'r', encoding='utf-8') as f:
            dump_data = f.read()

        connection.cursor().execute(dump_data)
#
# @receiver(post_migrate, sender=apps.get_app_config('ulkeler'))
# def create_initial_data(sender, **kwargs):
#     # Check if the 'Ulkeler' table is empty
#     if Ulkeler.objects.count() == 0:
#         # List of countries
#         ulke_list = [
#             'ABD Virjin Adaları (ABD)',
#             'Afganistan',
#             'Almanya',
#             'Amerikan Samoası (ABD)',
#             'Andorra',
#             'Angola',
#             'Anguilla (Birleşik Krallık)',
#             'Antigua ve Barbuda',
#             'Arjantin',
#             'Arnavutluk',
#             'Aruba (Hollanda)',
#             'Avustralya',
#             'Avusturya',
#             'Azerbaycan',
#             'Bahamalar',
#             'Bahreyn',
#             'Bangladeş',
#             'Barbados',
#             'Batı Sahra',
#             'Belçika',
#             'Belize',
#             'Benin',
#             'Bermuda (Birleşik Krallık)',
#             'Beyaz Rusya',
#             'Bhutan',
#             'Birleşik Arap Emirlikleri',
#             'Birleşik Krallık',
#             'Bolivya',
#             'Bosna-Hersek',
#             'Botsvana',
#             'Bouvet Adası (Norway)',
#             'Brezilya',
#             'Britanya Hint Okyanusu Toprakları (Birleşik Krallık)',
#             'Britanya Virjin Adaları (Birleşik Krallık)',
#             'Brunei',
#             'Bulgaristan',
#             'Burkina Faso',
#             'Burma',
#             'Burundi',
#             'Cayman Adaları (Birleşik Krallık)',
#             'Cebelitarık (Birleşik Krallık)',
#             'Cezayir',
#             'Christmas Adası (Avustralya)',
#             'Cibuti',
#             'Cocos Adaları (Avustralya)',
#             'Cook Adaları (Yeni Zelanda)',
#             'Curaçao (Hollanda)',
#             'Çad',
#             'Çek Cumhuriyeti',
#             'Çin',
#             'Danimarka',
#             'Demokratik Kongo Cumhuriyeti',
#             'Doğu Timor',
#             'Dominik Cumhuriyeti',
#             'Dominika',
#             'Ekvador',
#             'Ekvator Ginesi',
#             'El Salvador',
#             'Endonezya',
#             'Eritre',
#             'Ermenistan',
#             'Estonya',
#             'Etiyopya',
#             'Falkland Adaları (Birleşik Krallık)',
#             'Faroe Adaları (Danimarka)',
#             'Fas',
#             'Fiji',
#             'Fildişi Sahili',
#             'Filipinler',
#             'Filistin',
#             'Finlandiya',
#             'Fransa',
#             'Fransız Güney ve Antarktika Toprakları (Fransa)',
#             'Fransız Polinezyası (Fransa)',
#             'Gabon',
#             'Gambiya',
#             'Gana',
#             'Gine',
#             'Gine Bissau',
#             'Grenada',
#             'Grönland (Danimarka)',
#             'Guam (ABD)',
#             'Guatemala',
#             'Guernsey (Birleşik Krallık)',
#             'Guyana',
#             'Güney Georgia ve Güney Sandwich Adaları (Birleşik Krallık)',
#             'Güney Kore',
#             'Güney Sudan',
#             'Gürcistan',
#             'Haiti',
#             'Hırvatistan',
#             'Hindistan',
#             'Hollanda',
#             'Honduras',
#             'Hong Kong (Çin)',
#             'Irak',
#             'İran',
#             'İrlanda',
#             'İspanya',
#             'İsrail',
#             'İsveç',
#             'İsviçre',
#             'İtalya',
#             'İzlanda',
#             'Jamaika',
#             'Japonya',
#             'Jersey (Birleşik Krallık)',
#             'Kamboçya',
#             'Kamerun',
#             'Kanada',
#             'Karadağ',
#             'Katar',
#             'Kazakistan',
#             'Kenya',
#             'Kıbrıs Cumhuriyeti',
#             'Kırgızistan',
#             'Kiribati',
#             'Kolombiya',
#             'Komorlar',
#             'Kongo Cumhuriyeti',
#             'Kosta Rika',
#             'Kuveyt',
#             'Kuzey Kıbrıs Türk Cumhuriyeti',
#             'Kuzey Kore',
#             'Kuzey Mariana Adaları (ABD)',
#             'Küba',
#             'Laos',
#             'Lesoto',
#             'Letonya',
#             'Liberya',
#             'Libya',
#             'Lihtenştayn',
#             'Litvanya',
#             'Lübnan',
#             'Lüksemburg',
#             'Macaristan',
#             'Madagaskar',
#             'Makao (Çin)',
#             'Kuzey Makedonya',
#             'Malavi',
#             'Maldivler',
#             'Malezya',
#             'Mali',
#             'Malta',
#             'Man Adası (Birleşik Krallık)',
#             'Marshall Adaları',
#             'Mauritius',
#             'Meksika',
#             'Mısır',
#             'Mikronezya Federal Devletleri',
#             'Moğolistan',
#             'Moldova',
#             'Monako',
#             'Montserrat (Birleşik Krallık)',
#             'Moritanya',
#             'Mozambik',
#             'Namibya',
#             'Nauru',
#             'Nepal',
#             'Nijer',
#             'Nijerya',
#             'Nikaragua',
#             'Niue (Yeni Zelanda)',
#             'Norfolk Adası (Avustralya)',
#             'Norveç',
#             'Orta Afrika Cumhuriyeti',
#             'Özbekistan',
#             'Pakistan',
#             'Palau',
#             'Panama',
#             'Papua Yeni Gine',
#             'Paraguay',
#             'Peru',
#             'Pitcairn Adaları (Birleşik Krallık)',
#             'Polonya',
#             'Portekiz',
#             'Porto Riko (ABD)',
#             'Romanya',
#             'Ruanda',
#             'Rusya',
#             'Saint Barthélemy (Fransa)',
#             'Saint Helena (Birleşik Krallık)',
#             'Saint Kitts ve Nevis',
#             'Saint Lucia',
#             'Saint Martin (Fransa)',
#             'Saint Pierre ve Miquelon (Fransa)',
#             'Saint Vincent ve Grenadinler',
#             'Samoa',
#             'San Marino',
#             'São Tomé ve Príncipe',
#             'Senegal',
#             'Seyşeller',
#             'Sırbistan',
#             'Sierra Leone',
#             'Singapur',
#             'Sint Maarten (Hollanda)',
#             'Slovakya',
#             'Slovenya',
#             'Solomon Adaları',
#             'Somali',
#             'Sri Lanka',
#             'Sudan',
#             'Surinam',
#             'Suriye',
#             'Suudi Arabistan',
#             'Svalbard ve Jan Mayen (Norveç)',
#             'Svaziland',
#             'Şili',
#             'Tacikistan',
#             'Tanzanya',
#             'Tayland',
#             'Togo',
#             'Tokelau (Yeni Zelanda)',
#             'Tonga',
#             'Tunus',
#             'Turks ve Caicos Adaları (Birleşik Krallık)',
#             'Tuvalu',
#             'Türkiye',
#             'Türkmenistan',
#             'Uganda',
#             'Ukrayna',
#             'Umman',
#             'Uruguay',
#             'Ürdün',
#             'Vanuatu',
#             'Vatikan',
#             'Venezuela',
#             'Vietnam',
#             'Wallis ve Futuna (Fransa)',
#             'Yemen',
#             'Yeni Kaledonya (Fransa)',
#             'Yeni Zelanda',
#             'Yunanistan',
#             'Zambiya',
#             'Zimbabve',
#             'ABD',
#             'Abhazya',
#             'Ağrotur ve Dikelya (Birleşik Krallık)',
#             'Ashmore ve Cartier Adaları (Avustralya)',
#             'Clipperton Adası (Fransa)',
#             'Dağlık Karabağ',
#             'Güney Afrika',
#             'Güney Osetya',
#             'Heard Adası ve McDonald Adaları (Avustralya)',
#             'Kosova',
#             'Mercan Denizi Adaları (Avustralya)',
#             'Navassa Adası (ABD)',
#             'Pasifik Uzak Adaları Deniz Ulusal Anıtı',
#             'Somaliland',
#             'Spratly Adaları (tartışmalı)',
#             'Tayvan',
#             'Transdinyester',
#             'Trinidad ve Tobago',
#             'Wake Adası (ABD)',
#             'Yeşil Burun Adaları',
#         ]
#
#         max_retry = 3  # Set the maximum number of retries
#         retry_count = 0
#
#         while retry_count < max_retry:
#             try:
#                 for ulke in ulke_list:
#                     Ulkeler.objects.create(UlkeAdi=ulke)
#                 break  # Exit the loop if data creation is successful
#
#             except Exception as e:
#                 retry_count += 1
#                 if retry_count >= max_retry:
#                     raise  # Raise the exception if the maximum retry count is reached

@receiver(post_migrate, sender=apps.get_app_config('kurumlar'))
def create_initial_data(sender, **kwargs):
    # Check if the 'Kurumturleri' table is empty
    if KurumTurleri.objects.count() == 0:
        # List of kurumturleri
        kurumturu_list = [
            '1980 Merkezi Makam',
            '1996 Merkezi Makam',
            '1980 Velayet Merkezi Makam',
            'Adalet Bakanlığı',
            'Dışişleri Bakanlığı',
            'İçişleri Bakanlığı',
            'Aile Bakanlığı',
            'Diğer Bakanlık',
            'Savcılık',
            'Aile Mahkemesi',
            'Asliye Hukuk Mahkemesi',
            'Sulh Hukuk Mahkemesi',
            'Bölge Adliye Mahkemesi',
            'İcra Müdürlüğü',
            'Yargıtay',
            'Mahkemesi',
            'Şahıs'
        ]

        max_retry = 10  # Set the maximum number of retries
        retry_count = 0

        while retry_count < max_retry:
            try:
                for kurumturadi in kurumturu_list:
                    KurumTurleri.objects.create(TurAdi=kurumturadi)
                break  # Exit the loop if data creation is successful

            except Exception as e:
                retry_count += 1
                if retry_count >= max_retry:
                    raise  # Raise the exception if the maximum retry count is reached



@receiver(post_migrate, sender=apps.get_app_config('Dosya'))
def create_initial_data(sender, **kwargs):
    # Check if the 'CocuklaYakinlikTurleri' table is empty
    if CocuklaYakinlikTurleri.objects.count() == 0:
        # List of turleri
        yakinlik_turu_list = [
            'Anne',
            'Baba',
            'Büyük anne / baba',
            'Diğer akraba',
            'Kurum',
            'Diğer',
        ]

        max_retry = 10  # Set the maximum number of retries
        retry_count = 0

        while retry_count < max_retry:
            try:
                for adi in yakinlik_turu_list:
                    CocuklaYakinlikTurleri.objects.create(adi=adi)
                break  # Exit the loop if data creation is successful

            except Exception as e:
                retry_count += 1
                if retry_count >= max_retry:
                    raise  # Raise the exception if the maximum retry count is reached


@receiver(post_migrate, sender=apps.get_app_config('Dosya'))
def create_initial_data(sender, **kwargs):
                    # Check if the 'CocugaBakimTurleri' table is empty
                    if CocugaBakimTurleri.objects.count() == 0:
                        # List of kurumturleri
                        bakim_turu_list = [
                            'Tek Başına Ana Bakıcı /Sole Primary Carer',
                            'Ortak Bakım /Joint Primary Carer',
                            'Ana Bakıcı Değil /Non - Primary Carer',
                        ]

                        max_retry = 10  # Set the maximum number of retries
                        retry_count = 0

                        while retry_count < max_retry:
                            try:
                                for adi in bakim_turu_list:
                                    CocugaBakimTurleri.objects.create(adi=adi)
                                break  # Exit the loop if data creation is successful

                            except Exception as e:
                                retry_count += 1
                                if retry_count >= max_retry:
                                    raise  # Raise the exception if the maximum retry count is reached






@receiver(post_migrate, sender=apps.get_app_config('Dosya'))
def create_initial_data(sender, **kwargs):
                    # Check if the 'NihaiSonucTurleri' table is empty
                    if NihaiSonucTurleri.objects.count() == 0:
                        # List of nihai sonuç
                        nihai_sonuc_turu_list = [
                            ('Merkezi Makam tarafından reddedilen dava'),
                            ('Çocuk izlenmiyor, Sözleşme dışı bir ülkeye veya başka bir Sözleşme ülkesine kadar izleniyor'),
                            ('Geri dönüş için gönüllü anlaşma'),
                            ('İadesizlik için gönüllü anlaşma'),
                            ('Yargı kararı – İade emri verildi'),
                            ('Yargı kararı – İade reddedildi'),
                            ('Askıda olması'),
                            ('Geri çekildi'),
                            ('Farklı çocuklar için çoklu sonuçlar veya farklı sonuçlar'),
                            ('Başvuranın herhangi bir işlem yapmaması nedeniyle dava kapatılmıştır'),
                            ('Diğer'),
                            ('Erişim/iletişim için gönüllü anlaşma'),
                            ('Yargı kararı – erişim/iletişim emri verildi'),
                            ('Yargı kararı – erişim/iletişim reddedildi'),
                        ]

                        max_retry = 10  # Set the maximum number of retries
                        retry_count = 0

                        while retry_count < max_retry:
                            try:
                                for adi in nihai_sonuc_turu_list:
                                    NihaiSonucTurleri.objects.create(adi=adi)
                                break  # Exit the loop if data creation is successful

                            except Exception as e:
                                retry_count += 1
                                if retry_count >= max_retry:
                                    raise  # Raise the exception if the maximum retry count is reached




@receiver(post_migrate, sender=apps.get_app_config('Dosya'))
def create_initial_data(sender, **kwargs):
                    # Check if the 'MahkemeRedNedenleri' table is empty
                    if MahkemeRedNedenleri.objects.count() == 0:
                        # List of nihai sonuç
                        mahkeme_red_nedenleri_list = [
                            ('a. Çocuk mutad olarak Talep Eden Ülkede ikamet etmiyor'),
                            ('b. Başvuranın velayet hakkı yoktu'),
                            ('c. Madde 12 (çocuğun yerleşimi)'),
                            ('d. Madde 13(1)(a) başvuranın velayet haklarını kullanmaması'),
                            ('e. Madde 13(1)(a) muvafakat'),
                            ('f. Madde 13(1)(a) rıza'),
                            ('g. Madde 13(1)(b) (ağır risk)'),
                            ('h. Madde 13(2) Çocuğun itirazları'),
                            ('i. Madde 20 (İnsan Hakları)'),
                            ('j. Yorumlar')
                        ]

                        max_retry = 10  # Set the maximum number of retries
                        retry_count = 0

                        while retry_count < max_retry:
                            try:
                                for adi in mahkeme_red_nedenleri_list:
                                    MahkemeRedNedenleri.objects.create(adi=adi)
                                break  # Exit the loop if data creation is successful

                            except Exception as e:
                                retry_count += 1
                                if retry_count >= max_retry:
                                    raise  # Raise the exception if the maximum retry count is reached



