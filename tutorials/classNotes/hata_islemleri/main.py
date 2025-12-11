"""
Python'da Hatalar ve Hata Türleri
---------------------------------
Python programları çalışırken iki temel hata tipi oluşabilir:

1. SyntaxError (Sözdizimi Hataları)
2. Exceptions (Çalışma Zamanı Hataları)

SyntaxError: Kod daha çalışmadan oluşan hatalardır.
Exception: Kod çalışırken oluşan hatalardır ve try/except ile yakalanabilir.
"""


# ------------------------------------------------------------
# 1. SyntaxError (Çalıştırmadan önce oluşur — try ile yakalanamaz)
# ------------------------------------------------------------
# print("Merhaba"   # -> Parantez kapatılmadığı için SyntaxError oluşur
# Python daha kodu yorumlarken durur, program çalışmaz.


# ------------------------------------------------------------
# 2. Runtime Exceptions (try/except ile yakalanabilen hatalar)
# ------------------------------------------------------------

import os
def exception_examples():

    print("\n--- ValueError ---")
    try:
        int("abc")   # sayı olmayan bir metni int'e çevirme
    except ValueError as e:
        print("ValueError yakalandı:", e)

    print("\n--- TypeError ---")
    try:
        sonuc = "5" + 3   # str + int yapılmaz
    except TypeError as e:
        print("TypeError yakalandı:", e)

    print("\n--- ZeroDivisionError ---")
    try:
        x = 10 / 0
    except ZeroDivisionError as e:
        print("ZeroDivisionError yakalandı:", e)

    print("\n--- FileNotFoundError ---")
    try:
        open("olmayan_dosya.txt")
    except FileNotFoundError as e:
        print("FileNotFoundError yakalandı:", e)

    print("\n--- IndexError ---")
    try:
        liste = [1, 2, 3]
        liste[5]
    except IndexError as e:
        print("IndexError yakalandı:", e)

    print("\n--- KeyError ---")
    try:
        sözlük = {"ad": "Erkan"}
        sözlük["yas"]
    except KeyError as e:
        print("KeyError yakalandı:", e)

    print("\n--- AttributeError ---")
    try:
        x = 10
        x.append(5)   # int değerinin append metodu yok
    except AttributeError as e:
        print("AttributeError yakalandı:", e)

    print("\n--- ImportError ---")
    try:
        import olmayan_modül
    except ImportError as e:
        print("ImportError yakalandı:", e)

    print("\n--- OSError (genel işletim sistemi hataları) ---")
    try:
        os.remove("olmayan_dosya.txt")
    except OSError as e:
        print("OSError yakalandı:", e)



# ------------------------------------------------------------
# 3. Birden fazla hatayı birlikte yakalamak
# ------------------------------------------------------------
def multi_catch():
    try:
        veri = int("x")
    except (ValueError, TypeError) as e:
        print("Birden fazla hata türü yakalandı:", e)



# ------------------------------------------------------------
# 4. Hata fırlatmak (raise)
# ------------------------------------------------------------
def custom_raise(x):
    if x < 0:
        raise ValueError("x negatif olamaz")
    return x



# ------------------------------------------------------------
# 5. Özel exception sınıfı oluşturmak
# ------------------------------------------------------------
class LimitError(Exception):
    """Kullanıcı tanımlı bir hata."""
    pass

def check_limit(value):
    if value > 100:
        raise LimitError("Limit aşıldı!")
    return value



# ------------------------------------------------------------
# 6. try/except/finally yapısı
# ------------------------------------------------------------
def try_finally_example():
    try:
        f = open("demo.txt", "w")
        f.write("test")
    except Exception as e:
        print("Hata:", e)
    finally:
        # hata olsa bile kesin çalışır
        f.close()
        print("Dosya kapatıldı.")



# ------------------------------------------------------------
# 7. Program çalıştırıldığında örnekleri çalıştır
# ------------------------------------------------------------
if __name__ == "__main__":
    exception_examples()
    multi_catch()

    print("\n--- raise örneği ---")
    try:
        custom_raise(-5)
    except ValueError as e:
        print("custom_raise hatası:", e)

    print("\n--- Custom Exception örneği ---")
    try:
        check_limit(150)
    except LimitError as e:
        print("LimitError yakalandı:", e)

    try_finally_example()
