import mysql.connector

# Veritabanı bağlantısı oluştur
db = mysql.connector.connect(
    host="localhost",
    port="3333",
    user="root",
    password="123456",
    database="new_schema"
)

# Veritabanı bağlantısını kontrol et
if db.is_connected():
    print("Veritabanına başarıyla bağlanıldı!")
else:
    print("Veritabanına bağlanırken hata oluştu!")


def insert_country(country_name):
    # Veritabanına bağlan
    cursor = db.cursor()

    # Ülke ekleme işlemi
    sql = "INSERT INTO Ulkeler (UlkeAdi) VALUES (%s)"
    val = (country_name,)
    cursor.execute(sql, val)

    # Veritabanındaki değişiklikleri kaydet
    db.commit()


def get_countries():
    # Veritabanına bağlan
    cursor = db.cursor()

    # Tüm ülkeleri getir
    cursor.execute("SELECT * FROM Ulkeler")
    countries = cursor.fetchall()

    return countries


def insert_child(child_data):
    # Veritabanına bağlan
    cursor = db.cursor()

    # Çocuk ekleme işlemi
    sql = "INSERT INTO Cocuklar (CocukAdi, Soyadi, DogumTarihi, Cinsiyet, AnneAdi, BabaAdi, IletisimBilgileri, Notlar, UlkesiID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (child_data["CocukAdi"], child_data["Soyadi"], child_data["DogumTarihi"], child_data["Cinsiyet"], child_data["AnneAdi"], child_data["BabaAdi"], child_data["IletisimBilgileri"], child_data["Notlar"], child_data["UlkesiID"])
    cursor.execute(sql, val)

    # Veritabanındaki değişiklikleri kaydet
    db.commit()


def get_children():
    # Veritabanına bağlan
    cursor = db.cursor()

    # Tüm çocukları getir
    cursor.execute("SELECT * FROM Cocuklar")
    children = cursor.fetchall()

    return children


def insert_legal_representative(rep_data):
    # Veritabanına bağlan
    cursor = db.cursor()

    # Yasal temsilci ekleme işlemi
    sql = "INSERT INTO YasalTemsilciler (Unvani, Adi, IkinciAdi, Soyadi, DogumTarihi, Cinsiyet, TelefonNumarasi1, TelefonNumarasi2, Eposta, Notlar, UlkesiID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (rep_data["Unvani"], rep_data["Adi"], rep_data["IkinciAdi"], rep_data["Soyadi"], rep_data["DogumTarihi"], rep_data["Cinsiyet"], rep_data["TelefonNumarasi1"], rep_data["TelefonNumarasi2"], rep_data["Eposta"], rep_data["Notlar"], rep_data["UlkesiID"])
    cursor.execute(sql, val)

    # Veritabanındaki değişiklikleri kaydet
    db.commit()


def get_legal_representatives():
    # Veritabanına bağlan
    cursor = db.cursor()

    # Tüm yasal temsilcileri getir
    cursor.execute("SELECT * FROM YasalTemsilciler")
    representatives = cursor.fetchall()

    return representatives


if __name__ == "__main__":
    # Ülke ekleme işlemi
    insert_country("Türkiye")
    insert_country("Almanya")

    # Çocuk ekleme işlemi
    child_data = {
        "CocukAdi": "Ali",
        "Soyadi": "Yılmaz",
        "DogumTarihi": "2005-01-15",
        "Cinsiyet": "Erkek",
        "AnneAdi": "Ayşe",
        "BabaAdi": "Mehmet",
        "IletisimBilgileri": "ali.yilmaz@example.com",
        "Notlar": "Alerjik",
        "UlkesiID": 1
    }
    insert_child(child_data)

    # Yasal temsilci ekleme işlemi
    rep_data = {
        "Unvani": "Avukat",
        "Adi": "Ahmet",
        "Soyadi": "Kaya",
        "DogumTarihi": "1978-05-20",
        "Cinsiyet": "Erkek",
        "TelefonNumarasi1": "5551112233",
        "Eposta": "ahmet.kaya@example.com",
        "UlkesiID": 2
    }
    insert_legal_representative(rep_data)

    # Tüm ülkeleri getir
    countries = get_countries()
    print("Tüm Ülkeler:")
    for country in countries:
        print(country)

    # Tüm çocukları getir
    children = get_children()
    print("\nTüm Çocuklar:")
    for child in children:
        print(child)

    # Tüm yasal temsilcileri getir
    representatives = get_legal_representatives()
    print("\nTüm Yasal Temsilciler:")
    for rep in representatives:
        print(rep)

    db.close()
