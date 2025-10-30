isim = "Erkan"

for harf in isim:
    print(harf, end="-")
print("\nProgram Finished...\n\n")


#==============program that prints the letters of the name that are not in the surname===============

name = "Erkan"
surName= "TURGUT"

for i in name.lower():
    if not i in surName.lower():
        print(i, end="-")
print("\nProgram Finished...\n\n")