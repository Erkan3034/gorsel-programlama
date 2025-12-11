s1 = int(input("Bölünen sayıyı girin: "))
s2 = int(input("Bölen sayıyı girin: "))

try:
    sonuc = s1 / s2
    print(f"{s1} / {s2} = {sonuc}")
except ZeroDivisionError:
    print("Hata: Bir sayı sıfıra bölünemez!")