import tkinter as tk

# Ana pencere
root = tk.Tk()
root.title("Tkinter Sticky Demo")
root.geometry("600x400")

# Grid yapısını responsive yapmak
for i in range(3):
    root.columnconfigure(i, weight=1)
    root.rowconfigure(i, weight=1)

# Ortak stil
def create_label(text, bg):
    return tk.Label(
        root,
        text=text,
        bg=bg,
        fg="white",
        font=("Arial", 12),
        relief="solid",
        borderwidth=1
    )

# 1️⃣ sticky="w"
lbl_w = create_label("sticky = 'w'\n(sola yaslanır)", "teal")
lbl_w.grid(row=0, column=0, sticky="w", padx=5, pady=5)

# 2️⃣ sticky="e"
lbl_e = create_label("sticky = 'e'\n(sağa yaslanır)", "purple")
lbl_e.grid(row=0, column=1, sticky="e", padx=5, pady=5)

# 3️⃣ sticky="ew"
lbl_ew = create_label("sticky = 'ew'\n(yatay genişler)", "orange")
lbl_ew.grid(row=0, column=2, sticky="ew", padx=5, pady=5)

# 4️⃣ sticky="ns"
lbl_ns = create_label("sticky = 'ns'\n(dikey genişler)", "brown")
lbl_ns.grid(row=1, column=0, sticky="ns", padx=5, pady=5)

# 5️⃣ sticky="nsew"
lbl_nsew = create_label("sticky = 'nsew'\n(hücresini doldurur)", "green")
lbl_nsew.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=5, pady=5)

root.mainloop()
