
""" 
Ucgen bulma Uygulaması
"""
a=int(input("1. Kenar Uzunluğunu Giriniz: ")) 
b=int(input("2. Kenar Uzunluğunu Giriniz: "))
c=int(input("3. Kenar Uzunluğunu Giriniz: "))

if a==b and b==c:
    print("INFO: Eşkenar Üçgen")
elif a==b or b==c or a==c:
    print("INFO: İkizkenar Üçgen")    
elif a+b>c and a+c>b and b+c>a:
    print("INFO: Üçgendir!")
else:
    print("INFO: Üçgen Değildir!")    
print("INFO: Program Finished...\n\n")
# End of the program


