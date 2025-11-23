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


