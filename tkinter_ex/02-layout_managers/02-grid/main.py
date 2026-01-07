import tkinter as tk
from tkinter import Label, Entry, Button
import random

"""
Grid = Excel tablosu gibi dusun

Satır → row

Sütun → column

Grid’de Hizalama (sticky)
tk.Label(root, text="Ad:").grid(row=0, column=0, sticky="w")

Değer | Anlam   |
----------------  
n     | yukarı  |
s     | aşağı   |
e     | sağ     |
w     | sol     |

"""
#============= pencere ayarlari =============
root = tk.Tk()
root.title("Grid Layout Manager")
root.geometry("400x300")

label = tk.Label(root, text="Ad:")
label.grid(row=0, column=0)

nameEntry = tk.Entry(root)
nameEntry.grid(row=0, column=1)

label2 = tk.Label(root, text="Soyad:")
label2.grid(row=1, column=0)

lastNameEntry = tk.Entry(root)
lastNameEntry.grid(row=1, column=1)

label3= tk.Label(root, text="")
label3.grid(row=3, column=0, columnspan=2)



def changeName():
    name = nameEntry.get()
    label3.config(text=name)

name_button = Button(root, text="Adı değiştir", command=changeName)
name_button.grid(row=2, column=0, columnspan=2)

root.mainloop()