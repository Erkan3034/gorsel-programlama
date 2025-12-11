try:
    s1 = int(input("Bölünen sayıyı girin: "))
    s2 = int(input("Bölen sayıyı girin: "))

    sonuc = s1 / s2
    print(f"{s1} / {s2} = {sonuc}")

except ValueError:
    print("Hata: Sayısal bir değer girmelisiniz.")

except ZeroDivisionError:
    print("Hata: Bir sayı sıfıra bölünemez!")

except Exception as hata:
    print("Beklenmeyen hata:", hata)
