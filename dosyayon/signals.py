# dosyayon/signals.py
from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from ulkeler.models import Ulkeler
from kurumlar.models import KurumTurleri
from dosyalar.models import CocuklaYakinlikTurleri, CocugaBakimTurleri, NihaiSonucTurleri, MahkemeRedNedenleri


import os
from django.db import connection
from django.dispatch import receiver

@receiver(post_migrate)
def import_data(sender, **kwargs):
    """
    Import initial data from a MySQL dump file.
    """
    dump_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'initial_data\countries-states-cities-Turkish-2023-8-12_1.sql')
    with open(dump_file_path, 'r', encoding='utf-8') as f:
        dump_data = f.read()

    connection.cursor().execute(dump_data)

@receiver(post_migrate, sender=apps.get_app_config('ulkeler'))
def create_initial_data(sender, **kwargs):
    # Check if the 'Ulkeler' table is empty
    if Ulkeler.objects.count() == 0:
        # List of countries
        ulke_list = [
            'ABD Virjin Adaları (ABD)',
            'Afganistan',
            'Almanya',
            'Amerikan Samoası (ABD)',
            'Andorra',
            'Angola',
            'Anguilla (Birleşik Krallık)',
            'Antigua ve Barbuda',
            'Arjantin',
            'Arnavutluk',
            'Aruba (Hollanda)',
            'Avustralya',
            'Avusturya',
            'Azerbaycan',
            'Bahamalar',
            'Bahreyn',
            'Bangladeş',
            'Barbados',
            'Batı Sahra',
            'Belçika',
            'Belize',
            'Benin',
            'Bermuda (Birleşik Krallık)',
            'Beyaz Rusya',
            'Bhutan',
            'Birleşik Arap Emirlikleri',
            'Birleşik Krallık',
            'Bolivya',
            'Bosna-Hersek',
            'Botsvana',
            'Bouvet Adası (Norway)',
            'Brezilya',
            'Britanya Hint Okyanusu Toprakları (Birleşik Krallık)',
            'Britanya Virjin Adaları (Birleşik Krallık)',
            'Brunei',
            'Bulgaristan',
            'Burkina Faso',
            'Burma',
            'Burundi',
            'Cayman Adaları (Birleşik Krallık)',
            'Cebelitarık (Birleşik Krallık)',
            'Cezayir',
            'Christmas Adası (Avustralya)',
            'Cibuti',
            'Cocos Adaları (Avustralya)',
            'Cook Adaları (Yeni Zelanda)',
            'Curaçao (Hollanda)',
            'Çad',
            'Çek Cumhuriyeti',
            'Çin',
            'Danimarka',
            'Demokratik Kongo Cumhuriyeti',
            'Doğu Timor',
            'Dominik Cumhuriyeti',
            'Dominika',
            'Ekvador',
            'Ekvator Ginesi',
            'El Salvador',
            'Endonezya',
            'Eritre',
            'Ermenistan',
            'Estonya',
            'Etiyopya',
            'Falkland Adaları (Birleşik Krallık)',
            'Faroe Adaları (Danimarka)',
            'Fas',
            'Fiji',
            'Fildişi Sahili',
            'Filipinler',
            'Filistin',
            'Finlandiya',
            'Fransa',
            'Fransız Güney ve Antarktika Toprakları (Fransa)',
            'Fransız Polinezyası (Fransa)',
            'Gabon',
            'Gambiya',
            'Gana',
            'Gine',
            'Gine Bissau',
            'Grenada',
            'Grönland (Danimarka)',
            'Guam (ABD)',
            'Guatemala',
            'Guernsey (Birleşik Krallık)',
            'Guyana',
            'Güney Georgia ve Güney Sandwich Adaları (Birleşik Krallık)',
            'Güney Kore',
            'Güney Sudan',
            'Gürcistan',
            'Haiti',
            'Hırvatistan',
            'Hindistan',
            'Hollanda',
            'Honduras',
            'Hong Kong (Çin)',
            'Irak',
            'İran',
            'İrlanda',
            'İspanya',
            'İsrail',
            'İsveç',
            'İsviçre',
            'İtalya',
            'İzlanda',
            'Jamaika',
            'Japonya',
            'Jersey (Birleşik Krallık)',
            'Kamboçya',
            'Kamerun',
            'Kanada',
            'Karadağ',
            'Katar',
            'Kazakistan',
            'Kenya',
            'Kıbrıs Cumhuriyeti',
            'Kırgızistan',
            'Kiribati',
            'Kolombiya',
            'Komorlar',
            'Kongo Cumhuriyeti',
            'Kosta Rika',
            'Kuveyt',
            'Kuzey Kıbrıs Türk Cumhuriyeti',
            'Kuzey Kore',
            'Kuzey Mariana Adaları (ABD)',
            'Küba',
            'Laos',
            'Lesoto',
            'Letonya',
            'Liberya',
            'Libya',
            'Lihtenştayn',
            'Litvanya',
            'Lübnan',
            'Lüksemburg',
            'Macaristan',
            'Madagaskar',
            'Makao (Çin)',
            'Kuzey Makedonya',
            'Malavi',
            'Maldivler',
            'Malezya',
            'Mali',
            'Malta',
            'Man Adası (Birleşik Krallık)',
            'Marshall Adaları',
            'Mauritius',
            'Meksika',
            'Mısır',
            'Mikronezya Federal Devletleri',
            'Moğolistan',
            'Moldova',
            'Monako',
            'Montserrat (Birleşik Krallık)',
            'Moritanya',
            'Mozambik',
            'Namibya',
            'Nauru',
            'Nepal',
            'Nijer',
            'Nijerya',
            'Nikaragua',
            'Niue (Yeni Zelanda)',
            'Norfolk Adası (Avustralya)',
            'Norveç',
            'Orta Afrika Cumhuriyeti',
            'Özbekistan',
            'Pakistan',
            'Palau',
            'Panama',
            'Papua Yeni Gine',
            'Paraguay',
            'Peru',
            'Pitcairn Adaları (Birleşik Krallık)',
            'Polonya',
            'Portekiz',
            'Porto Riko (ABD)',
            'Romanya',
            'Ruanda',
            'Rusya',
            'Saint Barthélemy (Fransa)',
            'Saint Helena (Birleşik Krallık)',
            'Saint Kitts ve Nevis',
            'Saint Lucia',
            'Saint Martin (Fransa)',
            'Saint Pierre ve Miquelon (Fransa)',
            'Saint Vincent ve Grenadinler',
            'Samoa',
            'San Marino',
            'São Tomé ve Príncipe',
            'Senegal',
            'Seyşeller',
            'Sırbistan',
            'Sierra Leone',
            'Singapur',
            'Sint Maarten (Hollanda)',
            'Slovakya',
            'Slovenya',
            'Solomon Adaları',
            'Somali',
            'Sri Lanka',
            'Sudan',
            'Surinam',
            'Suriye',
            'Suudi Arabistan',
            'Svalbard ve Jan Mayen (Norveç)',
            'Svaziland',
            'Şili',
            'Tacikistan',
            'Tanzanya',
            'Tayland',
            'Togo',
            'Tokelau (Yeni Zelanda)',
            'Tonga',
            'Tunus',
            'Turks ve Caicos Adaları (Birleşik Krallık)',
            'Tuvalu',
            'Türkiye',
            'Türkmenistan',
            'Uganda',
            'Ukrayna',
            'Umman',
            'Uruguay',
            'Ürdün',
            'Vanuatu',
            'Vatikan',
            'Venezuela',
            'Vietnam',
            'Wallis ve Futuna (Fransa)',
            'Yemen',
            'Yeni Kaledonya (Fransa)',
            'Yeni Zelanda',
            'Yunanistan',
            'Zambiya',
            'Zimbabve',
            'ABD',
            'Abhazya',
            'Ağrotur ve Dikelya (Birleşik Krallık)',
            'Ashmore ve Cartier Adaları (Avustralya)',
            'Clipperton Adası (Fransa)',
            'Dağlık Karabağ',
            'Güney Afrika',
            'Güney Osetya',
            'Heard Adası ve McDonald Adaları (Avustralya)',
            'Kosova',
            'Mercan Denizi Adaları (Avustralya)',
            'Navassa Adası (ABD)',
            'Pasifik Uzak Adaları Deniz Ulusal Anıtı',
            'Somaliland',
            'Spratly Adaları (tartışmalı)',
            'Tayvan',
            'Transdinyester',
            'Trinidad ve Tobago',
            'Wake Adası (ABD)',
            'Yeşil Burun Adaları',
        ]

        max_retry = 3  # Set the maximum number of retries
        retry_count = 0

        while retry_count < max_retry:
            try:
                for ulke in ulke_list:
                    Ulkeler.objects.create(UlkeAdi=ulke)
                break  # Exit the loop if data creation is successful

            except Exception as e:
                retry_count += 1
                if retry_count >= max_retry:
                    raise  # Raise the exception if the maximum retry count is reached

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
            '... Bakanlığı',
            'Savcılık',
            'Aile Mahkemesi',
            'Asliye Hukuk Mahkemesi',
            'Sulh Hukuk Mahkemesi',
            'Bölge Adliye Mahkemesi',
            'İcra Müdürlüğü',
            'Yargıtay',
            'Mahkemesi',
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



@receiver(post_migrate, sender=apps.get_app_config('dosyalar'))
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


@receiver(post_migrate, sender=apps.get_app_config('dosyalar'))
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






@receiver(post_migrate, sender=apps.get_app_config('dosyalar'))
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




@receiver(post_migrate, sender=apps.get_app_config('dosyalar'))
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



