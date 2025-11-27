import time

son_id = 3 # id artırımını otomaitk yaptırıyorum, her seferinde input almamak için
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
            f"{o['id']:<4}" # :<4 = 4 bosluk bırak
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
    tum_ogrencileri_goster()

    aranan_id= int(input("\n Güncellenecek öğrenci ID'si : "))

    for ogr in ogrenciler:
        if ogr["id"]== aranan_id:
            print("\n Mevcut Değeri Korumak İçin Boş Bırakabilirsiniz")
            yeni_ad = input("Ad: ") or ogr["ad"]
            yeni_soyad = input("Soyad: ") or ogr["soyad"]
            yeni_numara = input("Numara: ") or ogr["numara"]

            giris_yas = input("Yaş: ")
            yeni_yas = int(giris_yas) if giris_yas else ogr["yas"]

            yeni_email = input("E-mail: ") or ogr["e-mail"]
            

            ogr["ad"]=yeni_ad 
            ogr["soyad"]=yeni_soyad 
            ogr["numara"]=yeni_numara 
            ogr["yas"]=yeni_yas 
            ogr["e-mail"]=yeni_email 

            print("\nÖğrenci güncellendi!\n")
            return
    
    print("\nBu ID bulunamadı!\n")
            


def ogrenci_sil():
    tum_ogrencileri_goster()

    silinecek_id = int(input("\n Silmek istediğiniz öğrenci ID: "))
    
    try:
        for i in ogrenciler:
            if i["id"]: silinecek_id
            ogrenciler.remove(i)
            print("\n Öğrenci Başarıyla Silindi!\n")
            return
    except:
        print("\n Öğrenci Silinemedi ID kontrol edip tekrar deneyiniz!")

def menu():
    while True:
        print("********************Öğrenci Yönetim Sistemi************************\n")
        print("1. Tüm öğrencileri göster")
        print("2. Yeni öğrenci ekle")
        print("3. Öğrenci güncelle")
        print("4. Öğrenci sil")
        print("5. Çıkış")

        secim = input("Seçiminiz: ")

        if secim == "1":
            tum_ogrencileri_goster()
        elif secim == "2":
            ogrenci_ekle()
        elif secim == "3":
            ogrenci_guncelle()
        elif secim == "4":
            ogrenci_sil()
        elif secim == "5":
            print("\nSistem Kapatıldı.")
            break
        else:
            print("\nGeçersiz seçim!\n")


menu()