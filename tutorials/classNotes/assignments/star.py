"""
Yıldız Piramit Uygulaması
"""

n = int(input("Piramidin maksimum yıldız sayısını giriniz: "))

# Artan kısım (1'den n'e kadar)
i = 1
while i <= n:
    
    j = 1
    while j <= i:
        print("*", end="")
        j += 1
    print()  # Satır sonu
    i += 1

# Azalan kısım (n-1'den 1'e kadar)
i = n - 1
while i >= 1:
    j = 1
    while j <= i:
        print("*", end="")
        j += 1
    print()  # Satır sonu
    i -= 1

print("\nINFO: Program Finished...\n\n")
# End of the program

