# 🎓 Discord Bot Pencarian Data Mahasiswa
Bot Discord yang dibuat menggunakan discord.py untuk mencari dan menampilkan data mahasiswa dari database MySQL melalui slash command.

Dirancang untuk kebutuhan edukasi atau penggunaan internal kampus.

## ✨ Fitur
- 🔍 Pencarian profil mahasiswa berdasarkan NIM

- 🧑‍🎓 Pencarian profil mahasiswa berdasarkan Nama Lengkap

- 📚 Menampilkan daftar mahasiswa berdasarkan Angkatan

- ⏭️ Navigasi halaman menggunakan tombol Discord

- 🖼️ Tampilan profil menggunakan embed

- 🔐 Konfigurasi aman menggunakan file .env

## 🛠️ Teknologi
- Python 3.9+
- discord.py (Slash Commands)
- MySQL
- python-dotenv

## 📦 Instalasi
### 1. Clone repository
```bash
git clone https://github.com/yourusername/discord-student-bot.git
cd discord-student-bot
```

### 2. Install dependensi
```bash
pip install -r requirements.txt
```

# 🗄️ Struktur Database

Bot ini menggunakan tabel `mahasiswa` dengan kolom berikut:


| Kolom | Keterangan |
| :--- | :--- |
| NIM | Nomor Induk Mahasiswa |
| Nama | Nama Lengkap |
| Prodi | Program Studi |
| Fakultas | Fakultas |
| Angkatan | Tahun Angkatan |
| TTL | Tempat & Tanggal Lahir |
| Sosmed | Link Media Sosial |
| Foto_Url | URL Foto yang akan ditampilkan |

## 🚀 Menjalankan Bot
```bash
python bot.py
```

Jika berhasil, akan muncul pesan
```bash
Bot sudah online
```

## 🤖 Slash Command Tersedia

| Kolom | Keterangan |
| :--- | :--- | 
| /nim (NIM) | Cari data mahasiswa berdasarkan NIM |
| /nama (Nama) | Cari data mahasiswa berdasarkan nama lengkap |
| /list (angkatan) | Tampilkan daftar mahasiswa per angkatan berupa Nama dan NIM |

Berikut contoh pesan yang akan ditampilkan untuk pencarian menggunakan command nim/nama

![image](example)








## ⚠️ Catatan

Project ini hanya untuk keperluan edukasi dan internal.
Pastikan penggunaan data mahasiswa sesuai dengan aturan privasi yang berlaku.














## 📄 License
MIT License 
