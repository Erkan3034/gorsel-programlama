# --- Tuple (Demet) Ornekleri ---

# 1. Tuple Olusturma
# Tuple'lar () ile tanimlanir ve degistirilemez (immutable).
bos_tuple = ()
tek_elemanli = ("Elma",) # Tek elemanli ise virgul sart
meyveler = ("Elma", "Armut", "Kiraz", "Muz")
sayilar = 1, 2, 3, 4, 5 # Parantezsiz tanimlama (Packing)

print(" Tuple Cıktısı: Meyveler:", meyveler)
print(" Tuple Cıktısı: Sayilar:", sayilar)

# 2. Elemanlara Erisim
print("\n--- Elemanlara Erisim ---")
print(" Tuple Cıktısı: Ilk eleman:", meyveler[0])
print(" Tuple Cıktısı: Son eleman:", meyveler[-1])
print(" Tuple Cıktısı: Ilk iki eleman (Slicing):", meyveler[0:2])

# 3. Degistirilemezlik (Immutability)
print("\n--- Degistirilemezlik ---")
# meyveler[0] = "Karpuz" # Bu satir HATA verir: TypeError
print("Tuple elemanlari degistirilemez. meyveler[0] = 'Karpuz' hatali bir islemdir.")

# 4. Tuple Metodlari
print("\n--- Metodlar ---")
rakamlar = (1, 3, 5, 3, 7, 3)
print("Rakamlar:", rakamlar)
print("3 rakaminin sayisi (count):", rakamlar.count(3))
print("5 rakaminin indeksi (index):", rakamlar.index(5))

# 5. Unpacking (Paket Acma)
print("\n--- Unpacking ---")
koordinat = (10, 20)
x, y = koordinat
print(f"Koordinat: {koordinat} -> x: {x}, y: {y}")

# 6. Tuple ve List Karsilastirmasi
# Tuple daha az yer kaplar ve daha hizlidir.
import sys
liste_ornek = [1, 2, 3, 4, 5]
tuple_ornek = (1, 2, 3, 4, 5)

print(f"\nListe boyutu (byte): {sys.getsizeof(liste_ornek)}")
print(f"Tuple boyutu (byte): {sys.getsizeof(tuple_ornek)}")