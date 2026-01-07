import tkinter as tk

# 1. Ana pencere nesnesini oluşturma
pencere = tk.Tk()
pencere.title("İlk GUI Uygulamam") # Pencere başlığı
pencere.geometry("400x300")      # Pencere boyutu (Genişlik x Yükseklik)


label = tk.Label(pencere, text="Merhaba" , font=("Arial", 16))
label.pack(pady=20 , side="top")  # pady: Dikey boşluk bırakır


nameEntry= tk.Entry(pencere, text="İsminizi girin" ,  font=("Arial", 12))
nameEntry.pack(pady=10 ,side="bottom")


def greetUser():
    name = nameEntry.get()  # Entry içindeki veriyi al
    label.config(text=f"Merhaba, {name}" , fg="red")  # Label'ai güncelle


btn = tk.Button(pencere, text="Gönder", command=greetUser)
btn.pack(pady=10, side= "left")

# 2. Döngüyü başlatma (Pencerenin ekranda kalmasını sağlar)
pencere.mainloop()