import tkinter as tk

def selamla():
    yazi = "Merhaba " + giris.get()
    etiket.config(text=yazi, fg="blue")

pencere = tk.Tk()
pencere.geometry("300x200")

#Label
etiket = tk.Label(pencere, text="Adınızı yazın:", font="Arial 12")
etiket.pack(pady=10) # pady: Dikey boşluk bırakır

# Entry
giris = tk.Entry(pencere)
giris.pack(pady=5)

#Button
buton = tk.Button(pencere, text="Tıkla", command=selamla)
buton.pack(pady=10)

pencere.mainloop()