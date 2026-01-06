import tkinter as tk
from tkinter import Label, Entry, Button
import random

root = tk.Tk()
root.title("Pack Layout Manager")
root.geometry("400x300")
root.configure(bg="black")
root.resizable(True, True)

label = Label(root, text="Pack Layout Manager", font=("Arial", 16), fg="red")
label.pack(pady=20, padx=20) # pencere ortasina yerlestirir

numberLabel = Label(root, text="0", font=("Arial", 16), fg="green")
numberLabel.pack(pady=20, padx=20) # pencere ortasina yerlestirir

"""
pady = y ekseninde padding(ayarlama)
padx = x ekseninde padding(ayarlama)
"""
buton = Button(root, text="Programı Kapat.", command=root.destroy)
buton.pack(pady=20, padx=20) # pencere ortasina yerlestirir

buton2 = Button(root, text="Metin değiştir", command=lambda:label.config(text="Metin değiştirildi")).pack(pady=20, padx=20)


buton3 = Button(root, text="Sayır artır.", command=lambda:numberLabel.config(text=int(numberLabel['text']) + 1)).pack(pady=20, padx=20)

def change_bg_color():
    bg_colors = ['red','gray','green','black','yellow','blue','orange','pink','purple','brown','cyan','magenta']
    random_color = random.choice(bg_colors)
    root.configure(bg=random_color)
    print(f"Color changed!. Current color: {random_color}")

buton4  = Button(root, text = "Arkaplanı değiştir." , command = change_bg_color).pack(padx=20, pady=20)



root.mainloop()