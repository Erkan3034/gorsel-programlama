# -----------------------------------------------------------
# 1) DOSYA MODLARI (r, w, a, r+, w+, a+)
# -----------------------------------------------------------

"""
MODE AÇIKLAMALARI:

"r"  -> Dosyayı OKUMAK için açar. Dosya yoksa hata verir.
"w"  -> Dosyaya YAZMAK için açar. Dosyayı sıfırlar.
"a"  -> Dosyanın SONUNA EKLEME yapmak için açar.

"r+" -> Hem OKUR hem YAZAR, dosya sıfırlanmaz.
"w+" -> Hem okur hem yazar ama önce dosyayı SIFIRLAR.
"a+" -> Okur + yazar ama cursor hep SONDAN başlar.
"""


# -----------------------------------------------------------
# 2) ÖZEL DOSYA METOTLARI
# -----------------------------------------------------------

"""
file.read(size)      -> Dosyayı tamamen veya verilen kadar okur.
file.readline()      -> Tek bir satır okur.
file.readlines()     -> Tüm satırları liste olarak okur.

file.write(text)     -> Dosyaya yazı yazar.
file.writelines(list)-> Bir listeyi satır satır yazar.

file.seek(pos)       -> Cursor'u pos'a taşır.
file.tell()          -> Cursor'un anlık konumunu söyler.
file.close()         -> Dosyayı kapatır.
file.flush()         -> Buffer'daki veriyi hemen dosyaya yazar.
file.truncate(size)  -> Dosyayı kesip küçültür.
"""


# -----------------------------------------------------------
# 3) ÖRNEKLER
# -----------------------------------------------------------

# ------- Örnek 1: Dosya yazma (w) -------
with open("ornek.txt", "w") as file:
    file.write("Bu dosya 'w' modu ile oluşturuldu ve sıfırlandı.\n")
    file.write("İkinci satır eklendi.\n")


# ------- Örnek 2: Dosyaya ekleme (a) -------
with open("ornek.txt", "a") as file:
    file.write("Bu satır 'a' modu ile sona eklendi.\n")


# ------- Örnek 3: Dosyayı okuma (r) -------
with open("ornek.txt", "r") as file:
    print("=== DOSYA İÇERİĞİ ===")
    print(file.read())


# ------- Örnek 4: Satır satır okuma -------
with open("ornek.txt", "r") as file:
    print("\n=== SATIR SATIR OKUMA ===")
    for satir in file.readlines():
        print(satir.strip())


# ------- Örnek 5: seek + tell kullanımı -------
with open("ornek.txt", "r") as file:
    print("\nCursor ilk konum:", file.tell())

    file.seek(10)  # 10. byte'a git
    print("Cursor yeni konum:", file.tell())

    print("Bulunduğu yerden okunan kısım:", file.read())


# ------- Örnek 6: truncate ile dosyayı kesme -------
with open("ornek.txt", "a") as file:
    file.write("Fazla metin ekledik, kesilecek...\n")

with open("ornek.txt", "r+") as file:
    file.truncate(30)  # Dosyanın ilk 30 byte'ını bırak
    print("\nDosya truncate edildi (ilk 30 byte bırakıldı).")


# -----------------------------------------------------------
# 4) ASAL SAYI ÖRNEĞİ — 1'den 1000'e kadar asal sayıları dosyaya yazma
# -----------------------------------------------------------

def asal_mi(n: int) -> bool:
    """Verilen sayının asal olup olmadığını kontrol eder."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


with open("asal_sayilar.txt", "w") as file:
    for sayi in range(1, 1001):
        if asal_mi(sayi):
            file.write(str(sayi) + "\n")

print("\n1–1000 arasındaki asal sayılar 'asal_sayilar.txt' dosyasına yazıldı.")

