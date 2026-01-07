import os

# --------------------------------------------------
# Yardımcı fonksiyon: Başlık yazdırma
# --------------------------------------------------
def header(text):
    print(" " + "="*50)
    print(text)
    print("="*50)

# --------------------------------------------------
# 1) Dosya oluşturma ve içine yazma (write)
# --------------------------------------------------
def create_file():
    header("1) Dosya Oluşturma ve Yazma")
    with open("example.txt", "w", encoding="utf-8") as f:
        f.write("Merhaba Erkan! Bu bir dosya yazma örneğidir.")
    print("example.txt oluşturuldu ve içine yazıldı.")

# --------------------------------------------------
# 2) Dosya okuma
# --------------------------------------------------
def read_file():
    header("2) Dosya Okuma")
    with open("example.txt", "r", encoding="utf-8") as f:
        print(f.read())

# --------------------------------------------------
# 3) Dosyaya ekleme (append)
# --------------------------------------------------
def append_file():
    header("3) Dosyaya Ekleme (Append)")
    with open("example.txt", "a", encoding="utf-8") as f:
        f.write("Bu satır append ile eklendi.")
    print("Yeni satır eklendi.")

# --------------------------------------------------
# 4) 1–1000 arasındaki asal sayıları bulup dosyaya yazma
# --------------------------------------------------
def primes_to_file():
    header("4) 1–1000 Arası Asal Sayıları Yazma")

    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5)+1):
            if n % i == 0:
                return False
        return True

    primes = [str(i) for i in range(1, 1001) if is_prime(i)]

    with open("primes.txt", "w", encoding="utf-8") as f:
        f.write(" ".join(primes))

    print(f"Toplam {len(primes)} asal sayı primes.txt dosyasına yazıldı.")

# --------------------------------------------------
# 5) Dosya silme
# --------------------------------------------------
def delete_file():
    header("5) Dosya Silme")
    if os.path.exists("example.txt"):
        os.remove("example.txt")
        print("example.txt silindi.")
    else:
        print("Silinecek dosya bulunamadı.")

# --------------------------------------------------
# Basit Menü
# --------------------------------------------------
def menu():
    while True:
        print("--- MENÜ ---")
        print("1) Dosya oluştur ve yaz")
        print("2) Dosya oku")
        print("3) Dosyaya ekle")
        print("4) 1–1000 arası asal sayıları dosyaya yaz")
        print("5) Dosya sil")
        print("0) Çıkış")

        secim = input("Seçimin: ")

        if secim == "1": create_file()
        elif secim == "2": read_file()
        elif secim == "3": append_file()
        elif secim == "4": primes_to_file()
        elif secim == "5": delete_file()
        elif secim == "0":
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçim.")

# --------------------------------------------------
# Çalıştırma bloğu
# --------------------------------------------------
if __name__ == "__main__":
    print("Basit Dosya İşlemleri Rehberi")
    menu()
