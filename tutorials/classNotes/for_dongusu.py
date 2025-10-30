isim = "Erkan"

for harf in isim:
    print(harf, end="-")
print("\nLetters of the name Program Finished...\n\n")


#==============program that prints the letters of the name that are not in the surname===============

name = "Erkan"
surName= "TURGUT"

for i in name.lower():
    if not i in surName.lower():
        print(i, end="-")
print("\nLetters of the name that are not in the surname Program Finished...\n\n")


#============== find the consants and vowels in the inputted word===============

word = input("Enter a word: ")

consants = "bcdfghjklmnpqrstvwxyz"
vowels = "aeiou"
con_count = 0
vow_count = 0
for i in word:
    if i in vowels:
        vow_count += 1
    else:
        con_count += 1
print(f"Consants: {con_count}, Vowels: {vow_count}")
print("\nConsants and vowels in the inputted word Program Finished...\n\n")

#================== Program that prints the squares of the numbers in the list ==================

numbers = [1, 2, 3, 4, 5]
squares = []

for i in numbers:
    squares.append(i*i)
print(squares)
print("\nSquares of the numbers in the list Program Finished...\n\n")

#=========== 20den geriye doğru sayı yaazn program(range ile)
for i in range(20, 0, -1):
    print(i, end="-")
print("\nNumbers from 20 to 1 Program Finished...\n\n")

#=========== satır sütun yazdırma programı

a= int(input("Enter a column number : "))
b = int(input("Enter a row number : "))

for i in range (1,a+1):
    for j in range (1,b+1):
        print(j, end=" ")
    print()
print("\nRow and column print program Finished...\n\n")

#continue and break statements
for i in range(1, 10):
    if i == 5 or i == 6:
        continue
    if i == 8:
        break
    print(i, end=" ")
print("\nContinue and break statements Program Finished...\n\n")