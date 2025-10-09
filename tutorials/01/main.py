a=10

if a % 2 == 0:
     print(f"{a} is Even")
else:
     print(f"{a} is Odd")

print("Program Finished...\n\n")

# End of the program

b=20 
if a<b:
    print(f"{a} is less than {b}")
else:
    print(f"{a} is greater than {b}")
print("Program Finished...\n\n")

# End of the program

""" 
Ucgen bulma Uygulaması
"""
a=int(input("1. Kenar Uzunluğunu Giriniz: ")) 
b=int(input("2. Kenar Uzunluğunu Giriniz: "))
c=int(input("3. Kenar Uzunluğunu Giriniz: "))

if a==b and b==c:
    print("Eşkenar Üçgen")
elif a==b or b==c or a==c:
    print("İkizkenar Üçgen")    
elif a+b>c and a+c>b and b+c>a:
    print("INFO: Üçgendir!")
else:
    print("Üçgen Değildir!")    
print("Program Finished...\n\n")
# End of the program
