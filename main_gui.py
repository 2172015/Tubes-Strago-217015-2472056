import customtkinter as ctk

# Mengatur tema tampilan (Dark/Light)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Membuat jendela aplikasi utama
app = ctk.CTk()
app.geometry("400x200")
app.title("Aplikasi Pemilihan Tim E-Sport")

# Membuat fungsi sederhana saat tombol ditekan
def tombol_ditekan():
    label_teks.configure(text="Sistem B&B Siap Dibuat!")

# Menambahkan komponen teks (Label)
label_teks = ctk.CTkLabel(app, text="Halo, selamat datang di CustomTkinter!", font=("Arial", 16))
label_teks.pack(pady=20)

# Menambahkan komponen Tombol (Button)
tombol = ctk.CTkButton(app, text="Klik Saya", command=tombol_ditekan)
tombol.pack(pady=10)

# Menjalankan putaran aplikasi agar jendela tidak langsung menutup
app.mainloop()