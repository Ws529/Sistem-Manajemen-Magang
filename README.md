# Sistem Informasi Manajemen Magang & Portofolio Proyek (SIM-MPP)

![SIM-MPP Logo](theme/static/images/logo_diskominfo-kab-bekasi.png)

SIM-MPP adalah platform berbasis web yang dirancang khusus untuk mengelola aktivitas magang dan pameran portofolio proyek peserta magang di **Dinas Komunikasi, Informatika, Persandian, dan Statistik (Diskominfosantik) Kabupaten Bekasi**. Sistem ini mengintegrasikan pencatatan logbook harian, penugasan terstruktur, unggah karya portofolio, hingga penerbitan sertifikat digital yang aman dan transparan.

---

## 📸 Panduan Tangkapan Layar (Screenshots)

Untuk membuat README ini tampil profesional, Anda disarankan untuk menambahkan beberapa screenshot dari aplikasi Anda. 
1. Buat folder baru bernama `docs` di dalam root project Anda, lalu buat subfolder `screenshots` di dalamnya:
   `docs/screenshots/`
2. Ambil screenshot halaman-halaman berikut, ubah namanya sesuai daftar di bawah, lalu simpan ke folder `docs/screenshots/`:
   * **Halaman Login**: Simpan sebagai `login.png`
   * **Dashboard Mahasiswa**: Simpan sebagai `dashboard_mahasiswa.png`
   * **Dashboard Admin / Pembimbing**: Simpan sebagai `dashboard_admin.png`
   * **Daftar & Edit Logbook**: Simpan sebagai `logbook_page.png`
   * **Galeri Portofolio Proyek**: Simpan sebagai `portfolio_gallery.png`
   * **Validasi Sertifikat Magang**: Simpan sebagai `certificate_page.png`

---

## 🛠️ Fitur Utama Sistem

Sistem ini mendukung dua peran pengguna utama (*Role-Based Access Control*): **Mahasiswa (Peserta Magang)** dan **Admin (Pembimbing Lapangan)**.

### 1. Dashboard Interaktif & Dinamis
* **Mahasiswa**: Memantau progres logbook mingguan, daftar tugas aktif dari pembimbing, status verifikasi sertifikat, serta memiliki kemampuan mengubah warna tema visual banner dasbor (*Banner Color*).
* **Admin**: Menyediakan statistik ringkas secara *real-time* mengenai jumlah mahasiswa aktif, antrean validasi logbook, dan jumlah tugas tertunda.
> *Tempatkan screenshot dashboard di bawah ini:*
> 
> **Dashboard Admin:**
> ![Dashboard Admin](docs/screenshots/dashboard_admin.png)
> 
> **Dashboard Mahasiswa:**
> ![Dashboard Mahasiswa](docs/screenshots/dashboard_mahasiswa.png)

### 2. Manajemen & Validasi Logbook Harian
* **Pencatatan Kehadiran**: Mahasiswa dapat mencatat jenis kehadiran (`HADIR`, `IZIN_PERKULIAHAN`, `WFH`), deskripsi uraian pekerjaan, tautan hasil kerja, serta melampirkan gambar/dokumen pendukung.
* **Alur Validasi**: Logbook yang dikirim masuk status `MENUNGGU`. Admin meninjau dan dapat mengubah status menjadi `DISETUJUI` atau `REVISI` (disertai catatan umpan balik dan file koreksi).
* **Perbaikan Cepat**: Mahasiswa hanya dapat mengedit logbook yang ditolak (`REVISI`) untuk dikirimkan kembali ke pembimbing.
* **Ekspor Word**: Mahasiswa dapat mengunduh seluruh laporan logbook harian secara instan ke format file Microsoft Word (`.docx`).
> *Tempatkan screenshot halaman logbook di bawah ini:*
> 
> ![Manajemen Logbook](docs/screenshots/logbook_page.png)

### 3. Modul Penugasan Terstruktur
* Admin dapat membuat tugas baru lengkap dengan judul, deskripsi instruksi, batas waktu (*deadline*), dan memilih mahasiswa penerimanya.
* Mahasiswa dapat menandai tugas yang selesai dikerjakan dan mencantumkan tautan/file hasil kerja.

### 4. Galeri Portofolio Proyek
* Mahasiswa dapat memamerkan proyek yang mereka buat selama magang dengan mengunggah detail judul, kategori (contoh: *Web App, Mobile App*), teknologi, database yang digunakan, deskripsi, gambar sampul, serta tautan repositori (GitHub/GitLab).
* Admin dapat menyaring galeri portofolio berdasarkan kategori, teknologi, atau database secara dinamis (didukung AJAX).
> *Tempatkan screenshot galeri portofolio di bawah ini:*
> 
> ![Galeri Portofolio](docs/screenshots/portfolio_gallery.png)

### 5. Manajemen Sertifikat Kelulusan
* Admin dapat mengunggah sertifikat kelulusan digital, menginput nomor sertifikat resmi, dan menandainya sebagai terverifikasi.
* Mahasiswa dapat langsung mengunduh file sertifikat asli berformat PDF dari dashboard mereka.
> *Tempatkan screenshot sertifikat di bawah ini:*
> 
> ![Halaman Sertifikat](docs/screenshots/certificate_page.png)

### 6. Audit Trail & Log Aktivitas (Catatan Sistem)
* Merekam setiap operasi penting dalam basis data (`CREATE`, `UPDATE`, `DELETE`, `LOGIN`, `SYSTEM`) lengkap dengan informasi stempel waktu dan aktor yang bertanggung jawab untuk keperluan audit keamanan.

---

## 💻 Tech Stack & Integrasi

* **Backend Framework**: Django 6.0.4 (Python)
* **Frontend**: HTML5, Vanilla CSS, Tailwind CSS (melalui Django Tailwind), Bootstrap
* **Database**: MySQL (diakses via Django ORM)
* **Identity Management**: Firebase Authentication (sinkronisasi data login pengguna secara real-time)
* **Keamanan Tambahan**:
  * Integrasi **Google reCAPTCHA v2 & v3** untuk mengamankan formulir login/pendaftaran dari bot.
  * Kebijakan keamanan sesi bank-grade: Sesi otomatis terhapus saat browser ditutup, cookie sesi dibatasi maksimal 1 jam tanpa aktivitas, dan pembaruan sesi otomatis pada setiap interaksi.
  * Fitur wajib ganti kata sandi awal untuk pengguna baru.

---

## 🚀 Panduan Instalasi & Konfigurasi Lokal

Ikuti langkah-langkah di bawah ini untuk menjalankan SIM-MPP di komputer lokal Anda:

### 1. Kloning Repositori
```bash
git clone https://github.com/Username/Sistem-Manajemen-Magang.git
cd Sistem-Manajemen-Magang
```

### 2. Buat & Aktifkan Virtual Environment
* **Windows (PowerShell/CMD):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
* **Linux/macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instal Dependencies
Instal seluruh pustaka Python yang diperlukan:
```bash
pip install -r requirements.txt
```
*(Catatan: Jika file `requirements.txt` belum ada, jalankan `pip install django mysqlclient python-docx firebase-admin django-tailwind django-simple-captcha django-recaptcha python-dotenv`)*

### 4. Konfigurasi Environment File (`.env`)
Buat file bernama `.env` di folder root proyek Anda, lalu isi dengan konfigurasi berikut (silakan sesuaikan nilainya):



### 5. Konfigurasi Firebase Credentials
Pastikan file credential Firebase Admin SDK JSON disimpan dengan nama `firebase_credentials.json` di dalam direktori `sim_magang_portofolio/firebase_credentials.json`.

### 6. Migrasi Database & Buat Superuser
Pastikan server MySQL Anda (XAMPP/Laragon) sudah aktif dan buat database baru bernama `db_sim_mpp`. Kemudian jalankan:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 7. Jalankan Server
Anda dapat menjalankan server lokal menggunakan script batch otomatis:
```bash
# Klik dua kali file ini di Windows Explorer:
jalankan_server.bat
```
Atau jalankan secara manual menggunakan script Python:
```bash
python run.py
```
Server akan berjalan di host `0.0.0.0:8000` sehingga dapat diakses oleh komputer host via `http://127.0.0.1:8000/` maupun dari handphone/perangkat lain yang berada di dalam satu jaringan Wi-Fi yang sama menggunakan alamat IP lokal Anda yang akan tercetak otomatis pada terminal.

---

## 📄 Lisensi
Proyek ini dilindungi di bawah lisensi [MIT License](LICENSE).
