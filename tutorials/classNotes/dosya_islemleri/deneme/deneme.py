file = open("veri.txt", "r")
content = file.read()

print(content)
file.close()


#===============OKUMA=================

with open ("primes_safe.txt", "r") as file:
    content = file.read()
    print(content)

#===============YAZMA=================

isim = input("Dosyaya yazılacak ismi girin: ")
dosya = open("isimler.txt","w")
dosya.write(isim)
dosya.close()


#================YAZMA APPEND=================

yeniİsim = input("Dosyaya eklenecek ismi girin: ")

yeniDosya =open("isimler.txt","a")
yeniDosya.write("\n"+yeniİsim)
yeniDosya.close()
