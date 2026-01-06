import tkinter as tk 
from tkinter import Label

root = tk.Tk() # pencere olustur
root.title("İlk Tkinter Uygulamam") # pencere basligi
root.geometry("400x300") # pencere boyutu
root.resizable(False, False) # pencere boyutunu degistirme


helloText = Label(root, text="Hello World", font=("Arial", 16), fg="red")
helloText.pack()



root.mainloop() # ana donguyu baslat



def helloUser():
    