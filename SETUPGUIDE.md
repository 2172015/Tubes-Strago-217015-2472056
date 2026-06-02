# Panduan Setup & Instalasi: Aplikasi Pemilihan Tim E-Sport 🎮

Aplikasi Desktop GUI ini dikembangkan menggunakan **Python** dan **CustomTkinter** untuk menyelesaikan masalah optimasi Pemilihan Tim E-Sport menggunakan algoritma **Branch & Bound**.

## 📋 Prasyarat Sistem

Sebelum menjalankan aplikasi ini, pastikan sistem Anda sudah memiliki:

- **Python 3.8 atau lebih baru** (Bisa diunduh di [python.org](https://www.python.org/))
- **Visual Studio Code (VS Code)** direkomendasikan sebagai _code editor_.
- Ekstensi **Python** terinstal di VS Code.

---

## 🚀 Langkah-Langkah Instalasi & Menjalankan Program

Ikuti langkah-langkah di bawah ini secara berurutan pada terminal komputer Anda:

### 1. Unduh / _Clone Repository_

Buka terminal dan lakukan _clone repository_ ini ke komputer lokal Anda (jika Anda menggunakan Git):

```bash
git clone [https://github.com/username-anda/Tubes-Strago-TimEsports.git](https://github.com/username-anda/Tubes-Strago-TimEsports.git)
cd Tubes-Strago-TimEsports

```

_(Lewati langkah ini jika Anda sudah memiliki folder proyeknya secara lokal)_

### 2. Buat _Virtual Environment_ (Direkomendasikan)

Untuk mencegah bentrok antar _library_ Python, sangat disarankan untuk membuat ruang virtual khusus proyek ini. Buka terminal di dalam VS Code, lalu jalankan:

```bash
python -m venv .venv

```

### 3. Aktivasi _Virtual Environment_

Aktifkan _virtual environment_ yang baru saja dibuat.

- **Untuk pengguna Windows (Command Prompt / PowerShell):**

```bash
.venv\Scripts\activate

```

- **Untuk pengguna Mac/Linux:**

```bash
source .venv/bin/activate

```

_(Ciri-ciri berhasil: Akan muncul tulisan `(.venv)` berwarna hijau di awal baris terminal Anda)._

### 4. Instalasi Pustaka (_Library_)

Setelah _environment_ aktif, instal pustaka antarmuka grafis (`customtkinter`) yang dibutuhkan oleh aplikasi ini:

```bash
pip install customtkinter

```

### 5. Jalankan Aplikasi

Jika semua proses di atas berhasil, jalankan program utama dengan perintah:

```bash
python main_gui.py

```

Jendela aplikasi Desktop GUI Pemilihan Tim E-Sport akan segera muncul di layar Anda.

---

## 🛠️ Penyelesaian Masalah (_Troubleshooting_)

- **Error: `pip is not recognized**`Jika terminal tidak mengenali perintah`pip`, coba gunakan perintah pemanggilan modul Python secara langsung:

```bash
python -m pip install customtkinter

```

atau

```bash
py -m pip install customtkinter

```

- **Error: `ModuleNotFoundError: No module named 'customtkinter'**`Ini berarti pustaka belum terinstal di dalam *Virtual Environment*. Pastikan terminal Anda sudah memunculkan tanda`(.venv)`sebelum melakukan proses instalasi`pip install customtkinter`.
- **Error: Execution Policy PowerShell (Windows)**
  Jika saat proses aktivasi `.venv` muncul tulisan merah _"...cannot be loaded because running scripts is disabled on this system"_, jalankan perintah ini di PowerShell Anda untuk memberikan izin:

```bash
Set-ExecutionPolicy Unrestricted -Scope CurrentUser

```

Lalu ulangi langkah aktivasi (Langkah 3).

---

**Pengembang:**

- Effrain David Martoyo (2472056)
- Dave Andrew (2172015)
