import customtkinter as ctk
import random
from tkinter import messagebox
from logika_tim import jalankan_branch_and_bound

# ==========================================
# PENGATURAN TEMA & JENDELA UTAMA
# ==========================================
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1300x850") 
app.title("Aplikasi Pemilihan Tim E-Sport - Branch & Bound")

# Variabel global
data_kandidat = []
langkah_tersimpan = []
indeks_langkah_saat_ini = 0

# ==========================================
# FUNGSI-FUNGSI LOGIKA ANTARMUKA
# ==========================================
def render_tabel_header():
    """Fungsi pembantu untuk merender ulang kepala tabel"""
    teks_data.configure(state="normal")
    teks_data.delete("1.0", "end")
    teks_data.insert("end", f"{'ID PEMAIN':<15} | {'BIAYA KONTRAK':<16} | {'POIN SKILL'}\n")
    teks_data.insert("end", "-"*55 + "\n")
    teks_data.configure(state="disabled")

def reset_data():
    """Mengosongkan seluruh data kandidat di memori dan layar"""
    global data_kandidat
    data_kandidat.clear()
    teks_data.configure(state="normal")
    teks_data.delete("1.0", "end")
    teks_data.insert("end", "Data belum di-generate atau ditambahkan.\n")
    teks_data.configure(state="disabled")

def generate_data():
    """Fitur Demo: Menghasilkan data pemain secara acak"""
    global data_kandidat
    data_kandidat.clear()
    
    pilihan_n = combo_n.get()
    n = int(pilihan_n.split(" ")[1]) 
    
    render_tabel_header()
    teks_data.configure(state="normal")
    
    for i in range(1, n + 1):
        biaya = random.randint(10, 50)  
        skill = random.randint(50, 100) 
        nama_id = f"Pemain-{i:02d}"
        data_kandidat.append({'id': nama_id, 'biaya': biaya, 'skill': skill})
        teks_data.insert("end", f"{nama_id:<15} | ${biaya:<15} | {skill}\n")
        
    teks_data.configure(state="disabled")

def tambah_pemain_manual():
    """Fitur Nyata: Menambahkan satu pemain dari input manual pengguna"""
    nama = entry_nama.get()
    biaya_str = entry_biaya_get.get()
    skill_str = entry_skill.get()

    # Validasi input kosong
    if not nama or not biaya_str or not skill_str:
        messagebox.showwarning("Peringatan", "Semua kolom manual (Nama, Biaya, Skill) harus diisi!")
        return

    # Validasi tipe data angka
    try:
        biaya = int(biaya_str)
        skill = int(skill_str)
    except ValueError:
        messagebox.showerror("Error", "Biaya dan Skill harus berupa angka bulat!")
        return

    # Jika tabel masih kosong, buat headernya dulu
    if not data_kandidat:
        render_tabel_header()

    # Masukkan ke memori
    data_kandidat.append({'id': nama, 'biaya': biaya, 'skill': skill})

    # Tampilkan ke layar
    teks_data.configure(state="normal")
    teks_data.insert("end", f"{nama:<15} | ${biaya:<15} | {skill}\n")
    teks_data.configure(state="disabled")

    # Bersihkan form input manual setelah berhasil ditambah
    entry_nama.delete(0, "end")
    entry_biaya_get.delete(0, "end")
    entry_skill.delete(0, "end")
    
    # Fokuskan kursor kembali ke kolom nama untuk input berikutnya
    entry_nama.focus()

def eksekusi_algoritma():
    global langkah_tersimpan, indeks_langkah_saat_ini
    
    if not entry_budget.get() or not entry_k.get():
        messagebox.showerror("Error", "Batas Anggaran dan Target K harus diisi!")
        return
        
    if not data_kandidat:
        messagebox.showerror("Error", "Data kandidat masih kosong! Tambahkan pemain secara manual atau generate data terlebih dahulu.")
        return

    try:
        budget = int(entry_budget.get())
        k_target = int(entry_k.get())
    except ValueError:
        messagebox.showerror("Error", "Anggaran dan K harus berupa angka bulat!")
        return

    if k_target < 5 or k_target > 10:
        messagebox.showerror("Error", "Ukuran tim (K) harus antara 5 hingga 10 pemain!")
        return

    teks_hasil.configure(state="normal")
    teks_hasil.delete("1.0", "end")
    teks_hasil.insert("end", "Memproses algoritma Branch & Bound...\n")
    app.update()

    hasil = jalankan_branch_and_bound(k_target, budget, data_kandidat)

    teks_hasil.delete("1.0", "end")
    if hasil['tim_terbaik']:
        teks_hasil.insert("end", "=== SOLUSI OPTIMAL DITEMUKAN ===\n")
        teks_hasil.insert("end", f"Tim Terpilih   : {', '.join(hasil['tim_terbaik'])}\n")
        teks_hasil.insert("end", f"Total Biaya    : ${hasil['biaya_terpakai']} (Batas: ${budget})\n")
        teks_hasil.insert("end", f"Total Skill    : {hasil['max_skill']} Poin\n")
    else:
        teks_hasil.insert("end", "=== TIDAK ADA SOLUSI ===\n")
        teks_hasil.insert("end", "Anggaran terlalu kecil atau jumlah pemain tidak mencukupi untuk memenuhi target K.\n")

    teks_hasil.insert("end", "\n=== RINGKASAN STATISTIK ===\n")
    teks_hasil.insert("end", f"Jumlah Node Dikunjungi : {hasil['nodes_visited']} Node\n")
    teks_hasil.insert("end", f"Waktu Eksekusi         : {hasil['waktu_eksekusi']:.5f} detik\n")
    teks_hasil.configure(state="disabled")
    
    langkah_tersimpan = hasil['langkah_langkah']
    indeks_langkah_saat_ini = 0
    
    if langkah_tersimpan:
        tampilkan_step_sekarang()
        btn_prev.configure(state="normal")
        btn_next.configure(state="normal")

def tampilkan_step_sekarang():
    teks_step.configure(state="normal")
    teks_step.delete("1.0", "end")
    teks_step.insert("end", langkah_tersimpan[indeks_langkah_saat_ini])
    teks_step.configure(state="disabled")
    
    lbl_indikator_step.configure(text=f"Langkah {indeks_langkah_saat_ini + 1} dari {len(langkah_tersimpan)}")

def step_maju():
    global indeks_langkah_saat_ini
    if indeks_langkah_saat_ini < len(langkah_tersimpan) - 1:
        indeks_langkah_saat_ini += 1
        tampilkan_step_sekarang()

def step_mundur():
    global indeks_langkah_saat_ini
    if indeks_langkah_saat_ini > 0:
        indeks_langkah_saat_ini -= 1
        tampilkan_step_sekarang()

# ==========================================
# RANCANGAN LAYOUT GUI
# ==========================================

# --- FRAME KIRI: PANEL PENGATURAN ---
frame_kiri = ctk.CTkFrame(app, width=380) # Lebar ditambah sedikit untuk menampung tab
frame_kiri.pack(side="left", fill="y", padx=15, pady=15)

lbl_judul = ctk.CTkLabel(frame_kiri, text="Pengaturan B&B", font=("Arial", 28, "bold"))
lbl_judul.pack(pady=(20, 10))

lbl_budget = ctk.CTkLabel(frame_kiri, text="Batas Anggaran ($):", font=("Arial", 18))
lbl_budget.pack(anchor="w", padx=20, pady=(5, 0))
entry_budget = ctk.CTkEntry(frame_kiri, placeholder_text="Contoh: 150", font=("Arial", 18), height=40)
entry_budget.pack(fill="x", padx=20, pady=5)

lbl_k = ctk.CTkLabel(frame_kiri, text="Target Ukuran Tim (K):", font=("Arial", 18))
lbl_k.pack(anchor="w", padx=20, pady=(10, 0))
entry_k = ctk.CTkEntry(frame_kiri, placeholder_text="Antara 5 - 10", font=("Arial", 18), height=40)
entry_k.pack(fill="x", padx=20, pady=5)

# --- TABVIEW KELOLA PEMAIN ---
tabview = ctk.CTkTabview(frame_kiri, height=200)
tabview.pack(fill="x", padx=20, pady=(15, 5))
tab_otomatis = tabview.add("Otomatis (Demo)")
tab_manual = tabview.add("Manual (Nyata)")

# Isi Tab Otomatis
lbl_n = ctk.CTkLabel(tab_otomatis, text="Ukuran Pool Pemain (N):", font=("Arial", 16))
lbl_n.pack(anchor="w", padx=10, pady=(10, 0))
combo_n = ctk.CTkOptionMenu(tab_otomatis, values=["Small 12", "Medium 18", "Large 24"], font=("Arial", 16), height=35)
combo_n.pack(fill="x", padx=10, pady=5)
btn_generate = ctk.CTkButton(tab_otomatis, text="Generate Data Acak", font=("Arial", 16, "bold"), fg_color="#2b8a3e", hover_color="#237032", height=40, command=generate_data)
btn_generate.pack(fill="x", padx=10, pady=(15, 10))

# Isi Tab Manual
entry_nama = ctk.CTkEntry(tab_manual, placeholder_text="Nama/ID Pemain", font=("Arial", 16), height=35)
entry_nama.pack(fill="x", padx=10, pady=(10, 5))

frame_input_angka = ctk.CTkFrame(tab_manual, fg_color="transparent")
frame_input_angka.pack(fill="x", padx=10, pady=5)

entry_biaya_get = ctk.CTkEntry(frame_input_angka, placeholder_text="Biaya ($)", font=("Arial", 16), height=35, width=100)
entry_biaya_get.pack(side="left", fill="x", expand=True, padx=(0, 5))

entry_skill = ctk.CTkEntry(frame_input_angka, placeholder_text="Skill (Poin)", font=("Arial", 16), height=35, width=100)
entry_skill.pack(side="right", fill="x", expand=True, padx=(5, 0))

btn_tambah = ctk.CTkButton(tab_manual, text="Tambah Pemain", font=("Arial", 16, "bold"), fg_color="#17a2b8", hover_color="#138496", height=40, command=tambah_pemain_manual)
btn_tambah.pack(fill="x", padx=10, pady=(15, 10))

# --- TOMBOL RESET & EKSEKUSI ---
btn_reset = ctk.CTkButton(frame_kiri, text="Kosongkan Daftar Pemain", font=("Arial", 16, "bold"), fg_color="#6c757d", hover_color="#5a6268", height=45, command=reset_data)
btn_reset.pack(fill="x", padx=20, pady=(10, 10))

btn_run = ctk.CTkButton(frame_kiri, text="JALANKAN ALGORITMA", font=("Arial", 20, "bold"), fg_color="#c92a2a", hover_color="#a62323", height=55, command=eksekusi_algoritma)
btn_run.pack(fill="x", padx=20, pady=10)


# --- FRAME KANAN: PANEL TAMPILAN DATA & HASIL ---
frame_kanan = ctk.CTkFrame(app)
frame_kanan.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=15)

lbl_data = ctk.CTkLabel(frame_kanan, text="Daftar Kandidat Pemain", font=("Arial", 24, "bold"))
lbl_data.pack(anchor="w", padx=20, pady=(15, 0))

teks_data = ctk.CTkTextbox(frame_kanan, height=220, font=("Courier New", 22))
teks_data.pack(fill="both", expand=True, padx=20, pady=5)
teks_data.insert("end", "Data belum di-generate atau ditambahkan.\n")
teks_data.configure(state="disabled")

lbl_hasil = ctk.CTkLabel(frame_kanan, text="Ringkasan Solusi Akhir", font=("Arial", 24, "bold"))
lbl_hasil.pack(anchor="w", padx=20, pady=(10, 0))

teks_hasil = ctk.CTkTextbox(frame_kanan, height=220, font=("Courier New", 22))
teks_hasil.pack(fill="x", padx=20, pady=5)
teks_hasil.insert("end", "Menunggu eksekusi algoritma...")
teks_hasil.configure(state="disabled")

lbl_recheck = ctk.CTkLabel(frame_kanan, text="Navigasi Step-by-Step (Log B&B)", font=("Arial", 24, "bold"), text_color="#0056b3")
lbl_recheck.pack(anchor="w", padx=20, pady=(15, 0))

teks_step = ctk.CTkTextbox(frame_kanan, height=150, font=("Courier New", 22))
teks_step.pack(fill="x", padx=20, pady=5)
teks_step.insert("end", "Log eksekusi algoritma akan muncul di sini.")
teks_step.configure(state="disabled")

frame_navigasi = ctk.CTkFrame(frame_kanan, fg_color="transparent")
frame_navigasi.pack(fill="x", padx=20, pady=(5, 15))

btn_prev = ctk.CTkButton(frame_navigasi, text="<< Sebelumnya", font=("Arial", 16, "bold"), width=150, height=40, state="disabled", command=step_mundur)
btn_prev.pack(side="left")

lbl_indikator_step = ctk.CTkLabel(frame_navigasi, text="Langkah 0 dari 0", font=("Arial", 18, "bold"))
lbl_indikator_step.pack(side="left", expand=True)

btn_next = ctk.CTkButton(frame_navigasi, text="Selanjutnya >>", font=("Arial", 16, "bold"), width=150, height=40, state="disabled", command=step_maju)
btn_next.pack(side="right")

# ==========================================
# MENJALANKAN APLIKASI
# ==========================================
if __name__ == "__main__":
    app.mainloop()