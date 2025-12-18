import tkinter as tk

# 1. Ana pencere nesnesini oluşturma
pencere = tk.Tk()
pencere.title("İlk GUI Uygulamam") # Pencere başlığı
pencere.geometry("400x300")      # Pencere boyutu (Genişlik x Yükseklik)

# 2. Döngüyü başlatma (Pencerenin ekranda kalmasını sağlar)
pencere.mainloop()