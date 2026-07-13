# Sistem Informasi Manajemen Magang & Portofolio Proyek 

![SIM-MPP Logo](theme/static/images/logo_diskominfo-kab-bekasi.png)

Sistem informasi manajemen magang & portofolio adalah platform berbasis web yang dirancang khusus untuk mengelola aktivitas magang dan pameran portofolio proyek peserta magang di **Dinas Komunikasi, Informatika, Persandian, dan Statistik (Diskominfosantik) Kabupaten Bekasi**. Sistem ini mengintegrasikan pencatatan logbook harian, penugasan terstruktur, unggah karya portofolio, hingga penerbitan sertifikat digital yang aman dan transparan.

Aplikasi ini dibangun menggunakan framework **Django** & **Tailwind CSS** dengan database **MySQL** yang dijalankan menggunakan **Laragon**.

---

## 📸 Dokumentasi Tangkapan Layar (Screenshots)

Berikut adalah visualisasi antarmuka Sistem Informasi Manajemen Magang & Portofolio Proyek (SIM-MPP):

### 🔑 Halaman Autentikasi (Login & Register)

#### 🧑‍🎓 Mahasiswa (Peserta)
* **Halaman Login Mahasiswa:**
  ![Login Mahasiswa](docs/screenshots/user%20%28peserta%29/login-user.png)
* **Halaman Pendaftaran (Register) Mahasiswa:**
  ![Register Mahasiswa](docs/screenshots/user%20%28peserta%29/register-user.png)

#### 🧑‍💼 Admin (Pembimbing Lapangan)
* **Halaman Login Admin:**
  ![Login Admin](docs/screenshots/admin%20%28pembimbing%20lapangan%29/login-admin.png)
* **Halaman Pendaftaran (Register) Admin:**
  ![Register Admin](docs/screenshots/admin%20%28pembimbing%20lapangan%29/register-admin.png)

---

## 🛠️ Fitur Utama Sistem

Sistem ini mendukung dua peran pengguna utama (*Role-Based Access Control*): **Mahasiswa (Peserta Magang)** dan **Admin (Pembimbing Lapangan)**.

### 1. Dashboard Interaktif & Dinamis
* **Mahasiswa**: Memantau progres logbook mingguan, daftar tugas aktif dari pembimbing, status verifikasi sertifikat, serta memiliki kemampuan mengubah warna tema visual banner dasbor (*Banner Color*).
* **Admin**: Menyediakan statistik ringkas secara *real-time* mengenai jumlah mahasiswa aktif, antrean validasi logbook, dan jumlah tugas tertunda.
> *Tampilan Dashboard:*
> 
> **Dashboard Admin:**
> ![Dashboard Admin](docs/screenshots/admin%20%28pembimbing%20lapangan%29/dashboard-admin.png)
> 
> **Dashboard Mahasiswa:**
> ![Dashboard Mahasiswa](docs/screenshots/user%20%28peserta%29/dashboard-user%28peserta%29.png)

### 2. Manajemen & Validasi Logbook Harian
* **Pencatatan Kehadiran**: Mahasiswa dapat mencatat jenis kehadiran (`HADIR`, `IZIN_PERKULIAHAN`, `WFH`), deskripsi uraian pekerjaan, tautan hasil kerja, serta melampirkan gambar/dokumen pendukung.
* **Alur Validasi**: Logbook yang dikirim masuk status `MENUNGGU`. Admin meninjau dan dapat mengubah status menjadi `DISETUJUI` atau `REVISI` (disertai catatan umpan balik dan file koreksi).
* **Perbaikan Cepat**: Mahasiswa hanya dapat mengedit logbook yang ditolak (`REVISI`) untuk dikirimkan kembali ke pembimbing.
* **Ekspor Word**: Mahasiswa dapat mengunduh seluruh laporan logbook harian secara instan ke format file Microsoft Word (`.docx`).
> *Tampilan Pencatatan & Validasi Logbook:*
> 
> **Pencatatan & Perbaikan Logbook (Mahasiswa):**
> ![Pencatatan & Perbaikan Logbook](docs/screenshots/user%20%28peserta%29/pencatatan%26perbaikan-logbook-user.png)
> 
> **Riwayat Logbook (Mahasiswa):**
> ![Riwayat Logbook](docs/screenshots/user%20%28peserta%29/riwayat-logbook-user.png)
> 
> **Validasi Logbook (Admin):**
> ![Validasi Logbook](docs/screenshots/admin%20%28pembimbing%20lapangan%29/logbook-peserta-admin.png)

### 3. Kustomisasi Profil & Pengaturan Pengguna
* **Kustomisasi Banner**: Pengguna dapat mengubah warna latar belakang banner profil secara instan.
* **Circular Photo Cropper**: Dilengkapi Cropper.js untuk memotong foto profil dengan rasio 1:1 berbentuk lingkaran sebelum disimpan.
* **Inisial Avatars**: Tombol hapus foto profil akan memicu inisial otomatis dari UI Avatars sebagai fallback.
> *Tampilan Profil & Pengaturan:*
> 
> **Pengaturan Profil (Mahasiswa):**
> ![Pengaturan Profil Mahasiswa](docs/screenshots/user%20%28peserta%29/pengaturan-user.png)
> 
> **Pengaturan Profil (Admin):**
> ![Pengaturan Profil Admin](docs/screenshots/admin%20%28pembimbing%20lapangan%29/pengaturan-admin.png)

### 4. Modul Penugasan Terstruktur
* Admin dapat membuat tugas baru lengkap dengan judul, deskripsi instruksi, batas waktu (*deadline*), dan memilih mahasiswa penerimanya.
* Mahasiswa dapat menandai tugas yang selesai dikerjakan dan mencantumkan tautan/file hasil kerja.
> *Tampilan Modul Penugasan:*
> 
> **Daftar Tugas (Mahasiswa):**
> ![Tugas Mahasiswa](docs/screenshots/user%20%28peserta%29/tugas-saya-user%28peserta%29.png)
> 
> **Penugasan (Admin):**
> ![Penugasan Admin](docs/screenshots/admin%20%28pembimbing%20lapangan%29/penugasan-admin.png)

### 5. Galeri Portofolio Proyek
* Mahasiswa dapat memamerkan proyek yang mereka buat selama magang dengan mengunggah detail judul, kategori (contoh: *Web App, Mobile App*), teknologi, database yang digunakan, deskripsi, gambar sampul, serta tautan repositori (GitHub/GitLab).
* Admin dapat menyaring galeri portofolio berdasarkan kategori, teknologi, atau database secara dinamis (didukung AJAX).
> *Tampilan Portofolio Proyek:*
> 
> **Portofolio Proyek (Mahasiswa):**
> ![Portofolio Proyek](docs/screenshots/user%20%28peserta%29/portofolio-proyek-user.png)
> 
> **Galeri Portofolio (Admin):**
> ![Galeri Portofolio](docs/screenshots/admin%20%28pembimbing%20lapangan%29/portofolio-admin.png)

### 6. Manajemen Sertifikat Kelulusan
* Admin dapat mengunggah sertifikat kelulusan digital, menginput nomor sertifikat resmi, dan menandainya sebagai terverifikasi.
* Mahasiswa dapat langsung mengunduh file sertifikat asli berformat PDF dari dashboard mereka.
> *Tampilan Sertifikat Kelulusan:*
> 
> **Sertifikat (Mahasiswa):**
> ![Sertifikat Mahasiswa](docs/screenshots/user%20%28peserta%29/sertifikat-user.png)
> 
> **Manajemen Sertifikat (Admin):**
> ![Sertifikat Admin](docs/screenshots/admin%20%28pembimbing%20lapangan%29/sertifikat-admin.png)

### 7. Pengawasan & Rekapitulasi Laporan (Admin)
* **Daftar Peserta Magang**: Menampilkan semua daftar mahasiswa aktif dan detail data instansi/universitas.
* **Rekap Laporan Performa**: Menyediakan statistik penyelesaian tugas dan logbook mahasiswa serta tombol unduh rekap data format CSV.
* **Audit Trail (Catatan Sistem)**: Mencatat riwayat operasional basis data secara real-time demi transparansi dan audit keamanan.
> *Tampilan Pengawasan & Laporan:*
> 
> **Daftar Peserta Magang:**
> ![Daftar Peserta Magang](docs/screenshots/admin%20%28pembimbing%20lapangan%29/data-peserta-admin.png)
> 
> **Rekap Laporan Performa:**
> ![Rekap Laporan Performa](docs/screenshots/admin%20%28pembimbing%20lapangan%29/laporan-admin.png)
> 
> **Catatan Sistem (Audit Log):**
> ![Catatan Sistem](docs/screenshots/admin%20%28pembimbing%20lapangan%29/catatan-sistem-admin.png)

### 8. Pusat Bantuan & Tutorial (Mahasiswa)
* Menyediakan panduan penggunaan sistem dan pintasan kontak bantuan kepada pengurus / admin.
> *Tampilan Pusat Bantuan:*
> 
> ![Pusat Bantuan & Tutorial](docs/screenshots/user%20%28peserta%29/support%26tutorial-user.png)

---

## 💻 Tech Stack & Integrasi

* **Backend Framework**: Django 6.0.4 (Python)
* **Frontend**: HTML5, Vanilla CSS, Tailwind CSS (melalui Django Tailwind), Bootstrap
* **Database**: MySQL (diakses via Django ORM, dijalankan menggunakan Laragon)
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

```env
# Google reCAPTCHA Keys
GOOGLE_CAPTCHA_SITE_KEY=isi_site_key_recaptcha_anda
GOOGLE_CAPTCHA_SECRET_KEY=isi_secret_key_recaptcha_anda

# Firebase Credentials
FIREBASE_API_KEY=isi_api_key_web_firebase_anda

# Django Secret Key
SECRET_KEY=isi_secret_key_django_acak

# MySQL Database Configuration
DB_NAME=db_sim_mpp
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306

# SMTP Email Configuration (Untuk pengiriman email aktivasi akun)
EMAIL_HOST_USER=email_pemberi_notifikasi@gmail.com
EMAIL_HOST_PASSWORD=isi_app_password_gmail_anda
```

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
