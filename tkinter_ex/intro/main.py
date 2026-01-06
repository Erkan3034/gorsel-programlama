import tkinter as tk 
from tkinter import Label, Entry, Button

root = tk.Tk() # pencere olustur
root.title("İlk Tkinter Uygulamam") # pencere basligi
root.geometry("400x300") # pencere boyutu
root.resizable(True, True) # pencere boyutunu degistirme


helloText = Label(root, text="Hello World", justify="center", font=("Arial", 16), fg="red")
helloText.pack(pady=20, padx=20) #

# Kullanicidan veri almak icin Entry
nameLabel = Label(root, text="Adinizi giriniz:", font=("Arial", 12))
nameLabel.pack(pady=10, padx=10)

nameEntry = Entry(root, justify="center", font=("Arial", 12))
nameEntry.pack(pady=10, padx=10)


# Soy isim
lastNameLabel = Label(root, text="Soyadinizi giriniz:", font=("Arial", 12))
lastNameLabel.pack(pady=10, padx=10)

lastNameEntry = Entry(root, justify="center", font=("Arial", 12))
lastNameEntry.pack(pady=10, padx=10)


def helloUser():
    name = nameEntry.get() # Entry icindeki veriyi al
    lastName = lastNameEntry.get()
    helloText.config(text=f"Hello, {name} {lastName}") # Label'i guncelle

# Buton
btn = Button(root, text="Gonder", command=helloUser)
btn.pack(pady=10, padx=10)

root.mainloop() # ana donguyu baslat