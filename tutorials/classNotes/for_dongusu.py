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