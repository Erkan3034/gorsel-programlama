import time

son_id = 0
ogrenciler =[
    {
        "id":1, "ad":"Erkan", "soyad":"TURGUT", "yas":22 , "numara":22010708048 , "e-mail":"22010708048@ogrenci.bartin.edu.tr"
    },
    {
         "id":2, "ad":"Serkan", "soyad":"TURGUT", "yas":24 ,"numara":22010708058 , "e-mail":"22010708058@ogrenci.bartin.edu.tr"
    }
]


def tum_ogrencileri_goster():
    if not ogrenciler:
        print("\nSistemde öğrenci bulunmuyor.\n")
        return
    
    print("\nID  Ad           Soyad         Numara         Yaş   Email")
    print("-" * 75)

    for o in ogrenciler:
        print(
            f"{o['id']:<4}"
            f"{o['ad']:<13}"
            f"{o['soyad']:<13}"
            f"{o['numara']:<17}"
            f"{str(o['yas']):<5}"
            f"{o['e-mail']}"
        )
    print()


def ogrenci_ekle():
    global son_id

    print("\n==============Yeni Öğrenci Ekle==============")
    ad = input("Öğrenci Adı: ")
    soyad = input("Öğrenci Soyadı: ")
    numara = input("Öğrenci Numarası(11 Hane): ")
    yas = int(input("Öğrenci Yaşı: "))
    e_mail=input("E-mail Adrsi: ")

    yeni_ogrenci={
        "id":son_id,
        "ad":ad,
        "soyad":soyad,
        "numara":numara,
        "yas":yas,
        "e-mail":e_mail
    }

    try:
        ogrenciler.append(yeni_ogrenci)
        son_id+=1
        print("\nÖğrenci Başarıyla Eklendi!\n")
    except:
        print("\nÖğrenci Eklenemedi, bilgileri kontrol edip tekrar denyin.\n")

def ogrenci_guncelle():
    