from tkinter import *

root = Tk()

root.title("Öğrenci Formu")
root.geometry("400x300")
root.configure(bg="lightblue")

frame = Frame(root, bg="white", padx=20, pady=20)
frame.pack(padx=30, pady=30, fill="x", expand=True)

name_var = StringVar()
age_var = StringVar()

def kontrol(*args):
    if name_var.get() and age_var.get():
        btn.config(text=f"Hoşgeldiniz {name_var.get()}, yaşınız {age_var.get()}.", 
                  fg="green", state=NORMAL)
    else:
        btn.config(text="Lütfen bilgilerinizi girin.", 
                  fg="red", state=DISABLED)

name_var.trace('w', kontrol)
age_var.trace('w', kontrol)

Label(frame, text="Adınız:", bg="white").pack(anchor="w")
Entry(frame, textvariable=name_var).pack(fill="x", pady=5)

Label(frame, text="Yaşınız:", bg="white").pack(anchor="w")
Entry(frame, textvariable=age_var).pack(fill="x", pady=5)



btn = Button(frame, text="Lütfen bilgilerinizi girin.", 
            fg="red", state=NORMAL)
btn.pack(pady=20)

root.mainloop()