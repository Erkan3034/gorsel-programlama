import tkinter as tk
from tkinter import StringVar

# ==================== PENCERE ====================
root = tk.Tk()
root.title("Mini Kayıt Uygulaması")
root.geometry("400x250")

# Grid sisteminde pencere büyüyünce
# içindeki frame'ler de büyüsün diye
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# ==================== FRAME'LER ====================
# Üst başlık alanı
header_frame = tk.Frame(root)
header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

# İçerik alanı (form)
content_frame = tk.Frame(root)
content_frame.grid(row=1, column=0, sticky="nsew", padx=10)

#Resutl alanı(sonuc label)
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

# Alt alan (buton)
footer_frame = tk.Frame(root)
footer_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

# İçerik frame'i de genişleyebilsin
content_frame.columnconfigure(1, weight=1)

# ==================== HEADER ====================
title_label = tk.Label(
    header_frame,
    text="Kullanıcı Kayıt Formu",
    font=("Arial", 14, "bold")
)
title_label.pack()

# ==================== STRINGVAR ====================
# Entry ile veri senkronu için kullanılır
name_var = StringVar()
age_var = StringVar()

# ==================== FORM (GRID) ====================
# Ad etiketi
tk.Label(content_frame, text="Ad:").grid(row=0, column=0, sticky="w", padx=5, pady=5)

# Ad giriş alanı
name_entry = tk.Entry(content_frame, textvariable=name_var)
name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

# Yaş etiketi
tk.Label(content_frame, text="Yaş:").grid(
    row=1, column=0, sticky="w", padx=5, pady=5
)

# Yaş giriş alanı
age_entry = tk.Entry(content_frame, textvariable=age_var)
age_entry.grid(
    row=1, column=1, sticky="ew", padx=5, pady=5
)

#===================== Sonuc ====================


# ==================== BUTON ====================
def kaydet():
    # StringVar içindeki değerlere erişiyoruz
    print("Ad:", name_var.get())
    print("Yaş:", age_var.get())

    result_label.config(text=f"Tebrikler! Kayıt yapıldı.", fg="green")

save_button = tk.Button(
    footer_frame,
    text="Kaydet",
    state="disabled",   # Başta pasif
    command=kaydet
)
save_button.pack()

# ==================== KONTROL MEKANİZMASI ====================
def alan_kontrol(*args):
    """
    Ad ve Yaş doluysa buton aktif olur
    """
    if name_var.get() and age_var.get():
        save_button.config(state="normal")
    else:
        save_button.config(state="disabled")

# StringVar değişince otomatik tetiklenir
name_var.trace_add("write", alan_kontrol)
age_var.trace_add("write", alan_kontrol)

# ==================== MAIN LOOP ====================
root.mainloop()
