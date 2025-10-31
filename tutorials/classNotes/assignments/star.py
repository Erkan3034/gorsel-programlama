"""
Yıldız Piramit Uygulaması
"""

n = int(input("Piramidin yüksekliğini giriniz: "))

i = 1
while i <= n:
    # Boşlukları yazdır
    j = 1
    while j <= n - i:
        print(" ", end="")
        j += 1
    
    # Yıldızları yazdır
    k = 1
    while k <= (2 * i - 1):
        print("*", end="")
        k += 1
    
    print()  # Satır sonu
    i += 1

print("\nINFO: Program Finished...\n\n")
# End of the program

