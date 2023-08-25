# dosyayon/signals.py
from django.apps import apps
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from random import randint
from kurumlar.models import KurumTurleri, Kurum
from Dosya.models import CocuklaYakinlikTurleri, CocugaBakimTurleri, NihaiSonucTurleri, MahkemeRedNedenleri
from yerler.models import Country, State, City
from cocuklar.models import Cocuk
from kisiler.models import Kisi
from Dosya.models import Dosya
from django.db.models.signals import pre_migrate
from django.apps import apps
import os
from django.db import connection
import random
from datetime import date, timedelta

from django.db.models.signals import post_migrate
from django.contrib.auth.models import User
from django.dispatch import receiver

data_already_populated = False  # Flag to track if data has been populated

names60 = [
    "Liam", "Olivia", "Noah", "Emma", "Mateo", "Sophia", "Muhammad", "Ava", "Oliver", "Isabella",
    "Santiago", "Mia", "Ethan", "Amelia", "Aiden", "Charlotte", "Luca", "Harper", "Sebastian", "Evelyn",
    "Zoe", "Lucas", "Luna", "Henry", "Mila", "Alexander", "Ella", "James", "Scarlett", "Benjamin", "Nova",
    "William", "Grace", "Leo", "Chloe", "Michael", "Penelope", "Daniel", "Sofia", "Carter", "Eleanor",
    "Aryan", "Emily", "David", "Layla", "Elijah", "Zara", "Ryan", "Avery", "Daniel", "Stella",
    "Mason", "Aria", "Sebastian", "Camila", "Ethan", "Mila", "James", "Lila", "Joseph", "Naomi",
    "Owen", "Ariana", "Jackson", "Elena", "Logan", "Hannah", "Alexander", "Nora", "Henry", "Leah",
    "Gabriel", "Abigail", "Samuel", "Addison", "John", "Audrey", "Nicholas", "Skylar", "Caleb", "Savannah",
    "Wyatt", "Victoria", "Matthew", "Claire", "Andrew", "Bella", "Joshua", "Lucy", "Nathan", "Paisley",
    "Isaac", "Violet", "Eli", "Lily", "Ezra", "Hazel", "Hunter", "Aubrey", "Evan", "Scarlett",
    "Mohammed", "Ahmed", "Ali", "Omar", "Hassan", "Abdullah", "Youssef", "Khalid", "Fadi", "Nasser",
    "Layla", "Amina", "Leila", "Fatima", "Sarah", "Yasmine", "Nour", "Samar", "Rana", "Hana",
    "Yusuf", "Hussein", "Zain", "Mahmoud", "Tariq", "Bilal", "Adnan", "Fahd", "Saad", "Nadir",
    "Zahra", "Aya", "Zara", "Dina", "Rima", "Lina", "Maha", "Farah", "Hala", "Dalal",
    "Kamal", "Nabil", "Tarek", "Jamal", "Rashid", "Hassan", "Sami", "Ibrahim", "Mustafa", "Fayez",
    "Amir", "Hamza", "Tariq", "Ismail", "Hadi", "Nadir", "Salem", "Ziad", "Anas", "Kareem",
    "Zahra", "Layla", "Amina", "Hana", "Jana", "Leila", "Nour", "Yara", "Mira", "Sara",
    "Yusuf", "Omar", "Ali", "Khalid", "Hussein", "Zain", "Fadi", "Saad", "Nadir", "Rami",
    "Rashid", "Zaid", "Tarek", "Fahd", "Hassan", "Sami", "Ibrahim", "Jamal", "Nabil", "Mustafa",
    "Yi", "Chen", "Hui", "Wei", "Jing", "Liang", "Xin", "Jun", "Ming", "Qing",
    "Xiu", "Yan", "Zhen", "Lei", "Yu", "Bo", "Fang", "Na", "Rui", "Zi",
    "Dan", "Hao", "Xiang", "Lan", "Tian", "Yun", "Jie", "Xing", "Mei", "Ning",
    "Wei", "Ying", "Kai", "Hong", "Rui", "Xia", "Xuan", "Chang", "Lin", "Yuan",
    "Yi", "Chen", "Hui", "Wei", "Jing", "Liang", "Xin", "Jun", "Ming", "Qing",
    "Xiu", "Yan", "Zhen", "Lei", "Yu", "Bo", "Fang", "Na", "Rui", "Zi",
    "Dan", "Hao", "Xiang", "Lan", "Tian", "Yun", "Jie", "Xing", "Mei", "Ning",
    "Wei", "Ying", "Kai", "Hong", "Rui", "Xia", "Xuan", "Chang", "Lin", "Yuan",
    "Zhang", "Li", "Wang", "Liu", "Chen", "Yang", "Zhao", "Huang", "Zhou", "Wu",

]

names61 = [
    "Lee", "Smith", "Johnson", "Brown", "Williams", "Jones", "Garcia", "Miller", "Davis", "Rodriguez",
    "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson",
    "Martin", "White", "Thompson", "Harris", "Garcia", "Allen", "Young", "Walker", "Hall", "King", "Wright",
    "Robinson", "Gonzalez", "Clark", "Lewis", "Johnson", "Hall", "Davis", "Turner", "Baker", "Green",
    "Hernandez", "Wood", "Ross", "Foster", "Ramirez", "Watson", "Morgan", "Cruz", "Peterson", "Cooper",
    "Reed", "Carter", "Howard", "Long", "Gray", "Kelly", "Powell", "Parker", "Cook", "Murphy",
    "Rogers", "Rogers", "Gomez", "Scott", "Diaz", "Morris", "Alexander", "Morris", "Reed", "Collins",
    "Bell", "Barnes", "Perez", "Coleman", "Phillips", "Perry", "Bennett", "Rogers", "Morgan", "Gray",
    "Stewart", "Brooks", "Russell", "Brooks", "Sanders", "Coleman", "Sanchez", "Edwards", "Turner", "Griffin",
    "Bryant", "Hughes", "Torres", "Mitchell", "Cox", "Butler", "Barnes", "Bennett", "James", "Peterson",

]

surnames62 = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
    "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
    "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King",
    "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter",
    "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins",
    "Stewart", "Sanchez", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell", "Cooper", "Peterson",
    "Bailey", "Rivera", "Cooper", "Richardson", "Cox", "Howard", "Ward", "Torres", "Peterson", "Gray",
    "Ramirez", "James", "Watson", "Brooks", "Kelly", "Sanders", "Price", "Bennett", "Wood", "Barnes",
    "Al-Mansoori", "Al-Batani", "Al-Khalil", "Al-Saud", "Al-Abdullah", "Al-Hashimi", "Al-Mazroui", "Al-Fahd",
    "Al-Shehri", "Al-Qasimi",
    "Al-Sulaimani", "Al-Ali", "Al-Maktoum", "Al-Jabri", "Al-Sayed", "Al-Hamad", "Al-Faisal", "Al-Mousa", "Al-Mahmoud",
    "Al-Haddad",
    "Al-Mansoori", "Al-Batani", "Al-Khalil", "Al-Saud", "Al-Abdullah", "Al-Hashimi", "Al-Mazroui", "Al-Fahd",
    "Al-Shehri", "Al-Qasimi",
    "Al-Sulaimani", "Al-Ali", "Al-Maktoum", "Al-Jabri", "Al-Sayed", "Al-Hamad", "Al-Faisal", "Al-Mousa", "Al-Mahmoud",
    "Al-Haddad",
    "Al-Mansoori", "Al-Batani", "Al-Khalil", "Al-Saud", "Al-Abdullah", "Al-Hashimi", "Al-Mazroui", "Al-Fahd",
    "Al-Shehri", "Al-Qasimi",
    "Al-Sulaimani", "Al-Ali", "Al-Maktoum", "Al-Jabri", "Al-Sayed", "Al-Hamad", "Al-Faisal", "Al-Mousa", "Al-Mahmoud",
    "Al-Haddad",
    "Al-Mansoori", "Al-Batani", "Al-Khalil", "Al-Saud", "Al-Abdullah", "Al-Hashimi", "Al-Mazroui", "Al-Fahd",
    "Al-Shehri", "Al-Qasimi",
    "Al-Sulaimani", "Al-Ali", "Al-Maktoum", "Al-Jabri", "Al-Sayed", "Al-Hamad", "Al-Faisal", "Al-Mousa", "Al-Mahmoud",
    "Al-Haddad",
    "Al-Mansoori", "Al-Batani", "Al-Khalil", "Al-Saud", "Al-Abdullah", "Al-Hashimi", "Al-Mazroui", "Al-Fahd",
    "Al-Shehri", "Al-Qasimi",
    "Al-Sulaimani", "Al-Ali", "Al-Maktoum", "Al-Jabri", "Al-Sayed", "Al-Hamad", "Al-Faisal", "Al-Mousa", "Al-Mahmoud",
    "Al-Haddad",
    "Zhang", "Li", "Wang", "Liu", "Chen", "Yang", "Zhao", "Huang", "Zhou", "Wu",
    "Xu", "Sun", "Ma", "Zhu", "Hu", "Guo", "He", "Gao", "Luo", "Lu",
    "Wei", "Jiang", "Shen", "Han", "Deng", "Qian", "Song", "Zheng", "Cao", "Tang",
    "Zhang", "Li", "Wang", "Liu", "Chen", "Yang", "Zhao", "Huang", "Zhou", "Wu",
    "Xu", "Sun", "Ma", "Zhu", "Hu", "Guo", "He", "Gao", "Luo", "Lu",
    "Wei", "Jiang", "Shen", "Han", "Deng", "Qian", "Song", "Zheng", "Cao", "Tang",
    "Yu", "Pan", "Dong", "Yuan", "Yao", "Liang", "Xie", "Wen", "Liang", "Feng"
]


@receiver(post_migrate)
def create_initial_kisiler(sender, **kwargs):
    if sender.name != 'kisiler':  # Replace 'your_app_name' with your actual app name
        return

    for _ in range(1000):
        kisi = Kisi.objects.create(
            Adi=f"Test {random.choice(names60)}",
            IkinciAdi=f"{random.choice(names61)}",
            Soyadi=random.choice(surnames62),
            DogumTarihi=date.today() - timedelta(days=random.randint(9125, 20175)),
            Cinsiyet=random.choice(['Erkek', 'Kız']),
            Ulkesi=Country.objects.get(pk=randint(1, 230)),
        )
        kisi.save()


NAMES_NEW = [
    "Eleanor", "Sebastian", "Aria", "Felix", "Lila", "Victor", "Zara", "Theodore", "Amara", "Adrian",
    "Luna", "Ezra", "Athena", "Maximus", "Evelyn", "Roman", "Elara", "August", "Cora", "Atticus",
    "Yusuf", "Azra", "Kuzey", "Elif", "Miray", "Aras", "Defne", "Can", "Aylin", "Emir",
    "Lucia", "Matias", "Sofía", "Leonardo", "Valentina", "Santiago", "Isabella", "Dante", "Emma", "Mariana",
    "Aylin", "Cem", "Elif", "Emir", "Ayşe", 
    "Kaan", "Zeynep", "Burak", "Leyla", "Eren", 
    "Deniz", "Ayla", "Can", "Merve", "Emre", 
    "Gizem", "Yasin", "Ela", "Berkay", "Ceren", 
    "Ali", "Selin", "Fırat", "Ebru", "Murat", 
    "Selma", "Baran", "Nazlı", "Sarp", "Esra", 
    "Arda", "İlayda", "Ozan", "Ayten", "Tolga", 
    "İpek", "Cihan", "Özlem", "Umut", "Nesrin", 
    "Hakan", "Asuman", "Ege", "Ezgi", "Tuna", 
    "İrem", "Caner", "Cansu", "Efe", "Gül", 
    "Mert", "İnci", "Kerem", "Nergis", "Eren", 
    "Yasemin", "İskender", "Meryem", "Emin", "Aysel", 
    "Uğur", "Feride", "Sinan", "Sevgi", "Okan", 
    "Ece", "Kadir", "Gonca", "Furkan", "Sibel", 
    "Enes", "Gizem", "Serkan", "Zehra", "Serdar", 
    "Pelin", "Oğuz", "Meltem", "Alper", "Dilara", 
    "Bora", "Derya", "Aydın", "Ayça", "Yiğit", 
    "Yasemin", "Batuhan", "Nihan", "Atakan", "Aslı", 
    "Erdem", "Begüm", "Koray", "Nil", "Yavuz", 
    "Cansel", "Emirhan", "Merve", "Sefa", "Didem", 
    "Ege", "Selin", "Arif", "Eda", "Kemal",
]



SURNAMES_NEW = [
    "Çalışkan", "Kara", "Yıldırım", "Aydın", "Başar", "Kaplan", "Demirci", "Altın", "Şahin", "Karaelmas",
    "Oktay", "Ergin", "Kıvanç", "Kocaman", "Kurtuluş", "Ergün", "Şensoy", "Yılmaz", "Can", "Köse",
    "Öztürk", "Karakaş", "Tekin", "Açıkgöz", "Gündüz", "Köksal", "Özen", "Akça", "Durmaz", "Göksel",
    "Aktaş", "Kapıcı", "Sarı", "Kaya", "Demir", "Çelik", "Aydın", "Şahin", "Aksoy", "Ergin",
    "Johnson", "Martinez", "Lee", "Garcia", "Zhang", "Silva", "Walker", "Nguyen", "Lopez", "Andersen",
    "Kaya", "Hansen", "Yılmaz", "Schmidt", "Gonzalez", "Sullivan", "Sato", "Ivanov", "Tan", "Ali",
    "O'Connor", "Sakamoto", "Smith", "Takahashi", "Wilson", "Santos", "Wang", "Peterson", "Arslan", "Fernandez",
    "Chen", "Larsen", "Koc", "Günay", "Miller", "Erdogan", "Wu", "Alves", "Yamamoto", "Kılıç", 
    "Smith", "Jones", "Taylor", "Brown", "Wilson", "Evans", "Patel", "Johnson", "Roberts", "Wright",
    "Walker", "Thompson", "White", "Hall", "Green", "Harris", "Young", "King", "Lee", "Turner",
    "Baker", "Clark", "Hill", "Cooper", "Carter", "Davis", "Murphy", "Price", "Morgan", "Cox",
    "Hughes", "Edwards", "Collins", "Stewart", "Morris", "Rogers", "Parker", "Bell", "Scott", "Adams",
    "Mitchell", "Cook", "Bailey", "Jackson", "Lewis", "Miller", "Martin", "Harrison", "Gray", "Wood",
    "Watson", "Bennett", "Richardson", "Grayson", "Robinson", "Cox", "Moore", "Bryant", "Turner", "Kelly",
    "Foster", "Hill", "Chapman", "Murray", "Webb", "Matthews", "Knight", "Wallace", "George", "Hunt",
    "Mills", "Powell", "Porter", "Holmes", "Mason", "Butler", "Taylor", "Harris", "Perry", "Jenkins",
    "Lawrence", "Cole", "Hawkins", "Hudson", "Fisher", "Simmons", "Reed", "Banks", "Barnes", "Davies"
    "Sato", "Suzuki", "Takahashi", "Tanaka", "Watanabe", "Ito", "Yamamoto", "Nakamura", "Kobayashi", "Kato",
    "Yoshida", "Yamada", "Sasaki", "Yamaguchi", "Matsumoto", "Inoue", "Kimura", "Hayashi", "Shimizu", "Saito",
    "Okada", "Mori", "Fujita", "Abe", "Ikeda", "Hashimoto", "Ishikawa", "Nakajima", "Maeda", "Fujii",
    "Ogawa", "Goto", "Kondo", "Shibata", "Nishimura", "Saito", "Murakami", "Nakagawa", "Sakamoto", "Maeda",
    "Endo", "Fujimoto", "Aoki", "Hirano", "Ota", "Miura", "Kudo", "Ueda", "Tamura", "Otsuka",
    "Chiba", "Maruyama", "Murata", "Ishii", "Kawaguchi", "Kondo", "Matsuda", "Nakano", "Harada", "Ono",
    "Yamashita", "Kaneko", "Sugiyama", "Takagi", "Nagai", "Wada", "Murata", "Saito", "Sugimoto", "Ishida",
    "Sakai", "Takada", "Ishii", "Noguchi", "Kondo", "Ota", "Ando", "Sugawara", "Tamura", "Kudo",
    "Yamada", "Takada", "Yamaguchi", "Ito", "Saito", "Nakamura", "Kawasaki", "Yoshida", "Kato", "Ogawa",
    "Kimura", "Ishikawa", "Sasaki", "Sato", "Fujita", "Nakajima", "Tanaka", "Yamamoto", "Mori", "Takahashi",

]


NAMES2 = [
    "Liam", "Olivia", "Noah", "Emma", "Mateo", "Sophia", "Muhammad", "Ava", "Oliver", "Isabella",
    "Santiago", "Mia", "Ethan", "Amelia", "Aiden", "Charlotte", "Luca", "Harper", "Sebastian", "Evelyn",
    "Zhang Wei", "Li Na", "Wang Wei", "Chen Wei", "Liu Wei", "Mohammed", "Sara", "Abdullah", "Amina",
    "Mia", "Ravi", "Leila", "Kavi", "Arya", "Rahul", "Anika", "Arjun", "Neha", "Dhruv", "Aisha",
    "Hiroshi", "Yuki", "Sakura", "Takashi", "Aiko", "Akio", "Haruko", "Riko", "Kazuki", "Yuna",
    "Matías", "Valentina", "Diego", "Camila", "Benjamín", "Isidora", "Nicolás", "Sofía", "Emiliano", "Amalia",
    "Hugo", "Lotte", "Finn", "Sofie", "Noor", "Aiden", "Ayaan", "Lila", "Zara", "Esmé",
    "Olaf", "Freja", "Lukas", "Emilie", "Jakob", "Maja", "Elias", "Isabella", "William", "Olivia",
    "Liam", "Emma", "Noah", "Ava", "Lucas", "Sophia", "Alexander", "Isabella", "Henry", "Mia",
    "Mateo", "Charlotte", "John", "Amelia", "Muhammad", "Harper", "Sebastian", "Evelyn", "Daniel", "Abigail",
    "Mohammed", "Chloe", "Oliver", "Emily", "Leo", "Elizabeth", "Kai", "Luna", "Ethan", "Grace"
    "Santiago", "Sophia", "Sebastian", "Isabella", "Matteo", "Olivia", "Emilio", "Mia", "Diego", "Emma",
    "Luis", "Ava", "Andres", "Luna", "Nico", "Camila", "Antonio", "Valentina", "Gabriel", "Julia",
    "Hiroshi", "Yuki", "Sakura", "Takashi", "Aiko", "Akio", "Haruko", "Riko", "Kazuki", "Yuna",
    "Rahul", "Anika", "Arjun", "Neha", "Aarav", "Priya", "Aryan", "Sara", "Aadit", "Zara",
    "Mateo", "Sofia", "Diego", "Camila", "Benjamín", "Isidora", "Nicolás", "Amelia", "Lucas", "Valentina",
    "Eduardo", "Catalina", "José", "Emilia", "Carlos", "Martina", "Javier", "Renata", "Manuel", "Ana",
    "Maximilian", "Sophie", "Liam", "Olivia", "Noah", "Emma", "Oliver", "Ava", "Ethan", "Isabella",
    "Aiden", "Mia", "Muhammad", "Sophia", "Lucas", "Amelia", "Alexander", "Harper", "James", "Evelyn",
    "Benjamin", "Liam", "William", "Oliver", "Henry", "Isabella", "Elijah", "James", "Daniel", "Charlotte",
    "Adam", "Ella", "Leo", "Aria", "Caleb", "Grace", "Michael", "Emily", "Oscar", "Lily",
]


@receiver(post_migrate)
def create_initial_cocuklar(sender, **kwargs):
    if sender.name != 'cocuklar':  # Replace 'cocuklar' with your actual app name
        return

    for _ in range(1000):

        cocuk = Cocuk.objects.create(
            Adi=f"Test {random.choice(NAMES_NEW)}",
            IkinciAdi=f"{random.choice(NAMES2)}",
            Soyadi=random.choice(SURNAMES_NEW),
            DogumTarihi=date.today() - timedelta(days=random.randint(300, 7000)),
            Cinsiyet=random.choice(['Erkek', 'Kız']),
            Ulkesi=Country.objects.get(pk=random.randint(1, 230)),
            # AnneAdi=Kisi.objects.get(pk=random.randint(1, 999)),
            # BabaAdi=Kisi.objects.get(pk=random.randint(1, 999)),
        )
        cocuk.save()



DOSYA_KODLARI = [
    ('A', 'A- 3-12-1980_IADE'),
    ('B', 'B- 3-12-1980-ILISKI'),
    ('C', 'C- 1996'),
    ('D', 'D- 3-13 (1980-VELAYET)'),
    ('E', 'E- 3-12-Bilgi'),
]


existing_combinations = set()  # Set to track unique combinations

@receiver(post_migrate)
def create_random_dosyalar(sender, **kwargs):
    global data_already_populated
    if sender.name != 'Dosya':  # Replace 'Dosya' with your actual app name
        return

    if not data_already_populated:

        for _ in range(5000):
            while True:
                dosya_kodu = random.choice(DOSYA_KODLARI)
                yil = random.randint(2010, 2023)
                sayi = random.randint(1, 20000)
                combination = f"{dosya_kodu[0]}-{yil}-{sayi}"
                if combination not in existing_combinations:
                    existing_combinations.add(combination)
                    break

            aciklama = f"Rastgele açıklama {_}"
            dosya_acilis_tarihi = date.today() - timedelta(days=random.randint(100, 3000))
            dosya_durumu = random.choice(['Açık', 'Kapalı', 'Arşiv'])
            dosya_kapanis_tarihi = None

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

            cocuk_objects = list(Cocuk.objects.all())
            sample_size = min(len(cocuk_objects), random.randint(1, 5))
            dosya.Cocuklar.set(random.sample(cocuk_objects, sample_size))

            dosya.save()

        data_already_populated = True



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




KURUM_LIST = [
    "Ankara 1. Asliye Hukuk Mahkemesi ", "Ankara Cumhuriyet Başsavcılığı", "Aile Bakanlığı", "Dışişliği Bakanlığı", "Almanya Merkezi Makamı"
]


@receiver(post_migrate)
def create_initial_kurumlar(sender, **kwargs):
    if sender.name != 'kurumlar':  # Replace 'your_app_name' with your actual app name
        return

    for _ in range(5):
        kurum = Kurum.objects.create(
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




@receiver(post_migrate)
def create_predefined_users(sender, **kwargs):
    if sender.name != 'auth':  # Replace 'auth' with your actual app name for User model
        return

    if User.objects.filter(username='admin').exists():
        # If the predefined user already exists, do not recreate it
        return

    # Create a predefined superuser
    superuser = User.objects.create_superuser('admin', 'admin@example.com', 'admin')

    # Create predefined regular users
    user_data = [
        {'username': 'birsen', 'email': 'birsen@example.com', 'password': '1'},
        {'username': 'cennet', 'email': 'ce@example.com', 'password': '1'},
        {'username': 'cemile', 'email': 'cem@example.com', 'password': '1'},
        # Add more predefined user data
    ]

    for data in user_data:
        User.objects.create_user(**data)



#
# @receiver(post_migrate)
# def create_initial_users(sender, **kwargs):
#     if sender.name != 'auth':  # Replace 'auth' with your actual app name for User model
#         return
#
#     if User.objects.filter(username='admin').exists():
#         # If the predefined user already exists, do not recreate it
#         return
#
#     predefined_users = [
#         {'username': 'admin', 'password': 'admin'},
#         {'username': 'birsen', 'password': '1'},
#         {'username': 'cennet', 'password': '1'},
#         {'username': 'cemile', 'password': '1'},
#         # Add more predefined users as needed
#     ]
#
#     for user_data in predefined_users:
#         username = user_data['username']
#         password = user_data['password']
#         User.objects.create_user(username=username, password=password)
