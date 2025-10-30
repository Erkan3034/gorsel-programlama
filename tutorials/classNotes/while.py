import random

sayac =1

while sayac <6:
    print("Merhaba Dünya")
    sayac +=1

print("\nINFO: Merhaba dünya döngüsü bitti\n")


#===============================

i =1
while i <6:
    print(i)
    i +=1
print("\nINFO: Artırma döngüsü bitti\n")
#===============================

#1den n sayısına kadar olan sayıların toplamını bulan program
n = int(input("1den n sayısına kadar olan sayıların toplamını bulan program\n"))
toplam = 0
i = 1  # HATA: i'nin değeri daha önce artırılmıştı ve burada sıfırlanmadı. Doğru çalışması için 1'den başlamalı.

while i <= n:
    toplam += i
    i += 1
print(f"1den {n} sayısına kadar olan sayıların toplamı: {toplam}")
print("Program Finished...\n\n")


#=============================


print("Sayı Tahmin Oyununa Hoşgeldin!")
alt_sinir = 1
ust_sinir = 100
sayi = random.randint(alt_sinir, ust_sinir)
tahmin_adet = 0


while True:
    tahmin = input(f"{alt_sinir} ile {ust_sinir} arasında bir sayı tahmin edin: ")
    if not tahmin.isdigit():
        print("Lütfen geçerli bir sayı giriniz.")
        continue
    tahmin = int(tahmin)
    tahmin_adet += 1

    if tahmin < sayi:
        print("Daha büyük bir sayı giriniz.")
    elif tahmin > sayi:
        print("Daha küçük bir sayı giriniz.")
    else:
        print(f"Tebrikler! {tahmin_adet}. denemede doğru tahmini buldunuz. Sayı: {sayi}")
        break

print("Oyun bitti. Tekrar oynayabilirsiniz!\n")

