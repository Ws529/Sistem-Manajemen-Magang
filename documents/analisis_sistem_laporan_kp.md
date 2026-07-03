# SUB-BAB: ANALISIS SISTEM (SIM-MPP)

Sub-bab ini menyajikan analisis sistem secara menyeluruh untuk **Sistem Informasi Manajemen Magang & Portofolio Proyek (SIM-MPP)** di Dinas Komunikasi, Informatika, Persandian, dan Statistik (Diskominfosantik) Kabupaten Bekasi. Analisis ini ditujukan untuk memberikan gambaran logis mengenai kebutuhan sistem, interaksi pengguna, aliran data, serta rancangan basis data yang diimplementasikan.

---

## 1. Konsep Sistem yang Diusulkan
SIM-MPP dirancang sebagai platform berbasis web yang mengintegrasikan pencatatan aktivitas harian peserta magang (*logbook*), pengelolaan penugasan oleh pembimbing, pengunggahan portofolio hasil proyek magang, hingga manajemen sertifikat akhir magang secara digital. Sistem ini dibangun menggunakan framework **Django (Python)** di sisi backend, **Vanilla CSS & Bootstrap** di sisi frontend, serta basis data relasional **MySQL** untuk penyimpanan data transaksional dan audit sistem. Selain itu, sistem diintegrasikan dengan **Firebase Authentication** untuk sinkronisasi manajemen identitas pengguna.

---

## 2. Analisis Sistem Berjalan (*As-Is*) vs Sistem Diusulkan (*To-Be*)

| Dimensi Analisis | Sistem Berjalan (*As-Is*) | Sistem Diusulkan (*To-Be*) |
| :--- | :--- | :--- |
| **Pencatatan Aktivitas** | Menggunakan lembar kerja fisik atau file Excel mandiri yang rentan hilang dan sulit dipantau secara real-time. | *Logbook* elektronik berbasis web yang dapat diisi setiap hari dan langsung masuk ke antrean validasi pembimbing. |
| **Monitoring Portofolio** | Hasil proyek peserta magang dikumpulkan secara manual via email/drive pribadi tanpa galeri terpusat. | Galeri portofolio terpusat yang dikelompokkan berdasarkan kategori proyek dan teknologi database yang digunakan. |
| **Pemberian Tugas** | Instruksi tugas diberikan secara lisan atau melalui aplikasi chat instan, sehingga batas waktu (*deadline*) sulit dipantau. | Modul penugasan digital lengkap dengan deskripsi, batas waktu, status pengerjaan (*Pending/Selesai*), serta umpan balik dari pembimbing. |
| **Validasi & Sertifikasi** | Verifikasi kehadiran dan kinerja dilakukan secara manual di akhir masa magang; pembuatan sertifikat memakan waktu lama. | Validasi harian oleh pembimbing lapangan melalui sistem. Unggah dan verifikasi sertifikat terintegrasi satu pintu. |
| **Catatan Keamanan & Audit** | Tidak ada perekaman aktivitas perubahan data (*audit trail*), mempersulit pelacakan jika terjadi kesalahan input. | Fitur *Log Aktivitas*/*Catatan Sistem* otomatis yang merekam operasi `CREATE`, `UPDATE`, `DELETE`, `LOGIN`, dan `SYSTEM` beserta aktornya. |

---

## 3. Analisis Kebutuhan Sistem

### A. Kebutuhan Fungsional (*Functional Requirements*)
Kebutuhan fungsional dikelompokkan berdasarkan hak akses pengguna (aktor):

#### 1. Aktor: Mahasiswa (Peserta Magang)
*   **F-MAH-01 (Autentikasi):** Mahasiswa dapat melakukan pendaftaran akun, melakukan aktivasi menggunakan kata sandi sementara yang dikirim lewat email, masuk (*login*), keluar (*logout*), dan melakukan pemulihan kata sandi (*reset password*).
*   **F-MAH-02 (Profil):** Mahasiswa dapat melihat dan memperbarui informasi profil pribadi, mengubah warna tema banner dashboard, serta mengganti kata sandi.
*   **F-MAH-03 (Entri Logbook):** Mahasiswa dapat mencatat aktivitas harian, menentukan kategori kehadiran (*HADIR*, *IZIN_PERKULIAHAN*, *WFH*), mengunggah tautan pendukung, serta melampirkan gambar/dokumen pendukung.
*   **F-MAH-04 (Perbaikan Logbook):** Mahasiswa dapat memperbaiki data logbook yang ditolak oleh pembimbing (status *REVISI*).
*   **F-MAH-05 (Ekspor Logbook):** Mahasiswa dapat mengekspor seluruh riwayat logbook ke dalam format dokumen Microsoft Word (`.docx`) secara otomatis.
*   **F-MAH-06 (Portofolio):** Mahasiswa dapat mengunggah portofolio proyek magang (judul, kategori, teknologi, database, deskripsi, gambar sampul, dan tautan repositori).
*   **F-MAH-07 (Tugas):** Mahasiswa dapat melihat daftar tugas dari pembimbing, memantau *deadline*, dan menandai tugas yang telah diselesaikan.
*   **F-MAH-08 (Dokumen & Bantuan):** Mahasiswa dapat mengunduh sertifikat magang yang telah divalidasi dan mengakses modul FAQ/bantuan.

#### 2. Aktor: Admin (Pembimbing / Validator Lapangan)
*   **F-ADM-01 (Dasbor Pemantauan):** Admin dapat melihat statistik ringkas jumlah mahasiswa, antrean validasi logbook, serta jumlah tugas tertunda secara *real-time*.
*   **F-ADM-02 (Manajemen Mahasiswa):** Admin dapat menambah, mengubah, menghapus (*soft delete/hard delete*), dan mengekspor data mahasiswa ke format CSV. Penambahan mahasiswa memicu pengiriman email aktivasi otomatis secara SMTP.
*   **F-ADM-03 (Validasi Logbook):** Admin dapat memeriksa logbook mahasiswa, memberikan status persetujuan (*MENUNGGU*, *REVISI*, *DISETUJUI*), serta memberikan catatan umpan balik dan file lampiran koreksi.
*   **F-ADM-04 (Evaluasi Portofolio):** Admin dapat memantau portofolio mahasiswa, menyaring portofolio berdasarkan kategori/teknologi, dan menghapus portofolio jika tidak sesuai standar.
*   **F-ADM-05 (Penugasan):** Admin dapat membuat tugas baru dengan menentukan mahasiswa penerima, judul, deskripsi, dan *deadline*, serta menghapus tugas.
*   **F-ADM-06 (Manajemen Sertifikat):** Admin dapat mengunggah file sertifikat magang untuk mahasiswa tertentu, menginput nomor sertifikat, dan memberikan status verifikasi.
*   **F-ADM-07 (Catatan Sistem / Audit Log):** Admin dapat memantau log aktivitas sistem (`LogAktivitas` / `CatatanSistem`) berdasarkan tipe operasi dan mengurutkannya secara kronologis.
*   **F-ADM-08 (Laporan & Pengaturan):** Admin dapat mengekspor rekapitulasi performa mahasiswa ke format Excel/CSV dan memperbarui informasi profil admin (NIP, unit kerja, jabatan, dan avatar).

---

### B. Kebutuhan Non-Fungsional (*Non-Functional Requirements*)
*   **Usability (Kemudahan Penggunaan):** Antarmuka responsif menggunakan basis layout modern (CSS Grid & Flexbox) dengan skema warna banner yang dapat diubah sesuai preferensi estetika pengguna (*banner color*).
*   **Security (Keamanan Informasi):**
    *   Autentikasi berlapis yang disinkronkan antara database lokal (enkripsi PBKDF2 bawaan Django) dengan Firebase Authentication.
    *   Penggunaan dekorator `@login_required` dan `@admin_required` (dengan metode penanganan 403 Forbidden agar sesi di tab browser lain tidak terputus) untuk mencegah *bypass* URL.
    *   Validasi berkas unggahan: pembatasan ukuran file pembimbing maksimal 10MB dan pembatasan ekstensi gambar foto profil hanya (.jpg, .jpeg, .png).
    *   Fitur wajib ganti sandi awal (*wajib_ganti_sandi*) saat pengguna pertama kali masuk sistem.
*   **Reliability (Keandalan):**
    *   Penanganan transaksi database terisolasi melalui ORM Django untuk mencegah inkonsistensi data.
    *   Pencegahan kegagalan aplikasi saat server SMTP mati dengan menyertakan blok *try-except* pada fungsi pengiriman email aktivasi.
*   **Portability (Portabilitas):** Ekspor laporan logbook dinamis ke Word (`.docx`) menggunakan pustaka `python-docx` di memori RAM (*in-memory buffer* via `io.BytesIO`) tanpa membebani penyimpanan fisik server.

---

## 4. Analisis Pengguna & Peran (*Actor Matrix*)

SIM-MPP membedakan otorisasi menggunakan pembagian peran (*role-based access control*):

1.  **Mahasiswa (ROLE = 'MAHASISWA'):** Peserta magang aktif yang memiliki akses ke modul pengisian logbook, pengerjaan tugas, pengunggahan portofolio proyek, pengunduhan sertifikat, serta pusat bantuan.
2.  **Admin (ROLE = 'ADMIN' / Superuser):** Pembimbing lapangan Diskominfosantik yang memiliki kontrol penuh atas manajemen data mahasiswa, validasi logbook, evaluasi portofolio proyek, pemberian tugas, verifikasi sertifikat, pemantauan log keamanan, dan ekspor laporan kerja.

---

## 5. Analisis Diagram Proses Bisnis (Berdasarkan Modul Draw.io)

### A. Activity Diagrams (Aliran Aktivitas)
Rancangan diagram aktivitas memetakan interaksi fungsional antara pengguna (aktor) dan sistem:

1.  **Activity Diagram - Dashboard Sistem SIM-MPP (`dashboard.xml`):**
    *   *Alur:* Pengguna mengakses halaman dashboard utama $\rightarrow$ Sistem memeriksa kredensial sesi dan peran pengguna $\rightarrow$ [Jika Admin] Sistem memuat grafik pendaftaran mahasiswa, antrean validasi logbook, dan status tugas aktif $\rightarrow$ [Jika Mahasiswa] Sistem memuat progres logbook pribadi, tugas aktif, dan status sertifikat $\rightarrow$ Merender halaman utama beserta widget visual.
2.  **Activity Diagram - Mengubah Kata Sandi Standar (`mengubah_kata_sandi_standar.xml`):**
    *   *Alur:* Pengguna masuk ke menu pengaturan keamanan $\rightarrow$ Pengguna memasukkan sandi lama dan sandi baru $\rightarrow$ Sistem memvalidasi sandi lama ke database MySQL $\rightarrow$ Jika tidak cocok, sistem menolak dan memunculkan pesan galat $\rightarrow$ Jika cocok, sistem mengenkripsi sandi baru, menyimpannya ke MySQL & Firebase Auth, lalu memicu pengiriman notifikasi email otomatis via SMTP.
3.  **Activity Diagram - Pencatatan & Perbaikan Logbook (`pencatatan_and_perbaikan_logbook.xml`):**
    *   *Alur:* Mahasiswa mengisi logbook harian (tanggal, uraian kerja, file lampiran) $\rightarrow$ Status awal diatur ke *MENUNGGU* $\rightarrow$ Admin memeriksa logbook $\rightarrow$ Jika disetujui, status diubah menjadi *DISETUJUI* $\rightarrow$ Jika ditolak, status diubah menjadi *REVISI* beserta catatan koreksi $\rightarrow$ Mahasiswa membuka kembali form entri logbook (hanya yang berstatus *REVISI* yang dapat dimodifikasi) $\rightarrow$ Mahasiswa memperbaiki data dan mengirim ulang $\rightarrow$ Status kembali ke *MENUNGGU*.
4.  **Activity Diagram - Pengelolaan Tugas (`tugas.xml`):**
    *   *Alur:* Admin membuka modul penugasan $\rightarrow$ Membuat tugas baru (judul, deskripsi, *deadline*, mahasiswa penerima) $\rightarrow$ Sistem menyimpan data ke MySQL dan memicu notifikasi $\rightarrow$ Mahasiswa melihat daftar tugas aktif di dashboard pribadi $\rightarrow$ Mahasiswa mengerjakan tugas dan mengunggah tautan/berkas jawaban $\rightarrow$ Admin meninjau berkas pengumpulan, mengisi nilai/skor dan catatan umpan balik $\rightarrow$ Nilai dan status diperbarui di database $\rightarrow$ Sistem menampilkan nilai akhir dan umpan balik pada dasbor mahasiswa.
5.  **Activity Diagram - Evaluasi Portofolio Proyek (`evaluasi_portofolio_proyek.xml`):**
    *   *Alur:* Admin membuka galeri portofolio $\rightarrow$ Admin menyaring data dengan menekan tombol kategori atau mengetik nama database/teknologi di kolom pencarian $\rightarrow$ Sistem mengeksekusi query filter ke database MySQL $\rightarrow$ Sistem memuat ulang tabel portofolio secara dinamis (AJAX) sesuai dengan parameter saringan.

### B. Sequence Diagrams (Urutan Interaksi Objek)
Rancangan diagram sekuen memetakan pesan yang dikirim antar-objek internal (User, View, Model, Database) selama siklus proses:

1.  **Sequence Diagram - Pengelolaan Portofolio (`pengelolaan_portofolio.xml`):**
    *   *Aktor:* Mahasiswa.
    *   *Alur:* Mahasiswa mengisi formulir di `portofolio_tambah.html` dan menekan submit $\rightarrow$ Mengirim POST request berisi data proyek dan file gambar sampul ke `PortfolioCreateView` $\rightarrow$ View menginstansiasi model `Portfolio` $\rightarrow$ Model menyimpan data ke database MySQL dan menyimpan gambar sampul ke penyimpanan media $\rightarrow$ Database membalas dengan konfirmasi penyimpanan sukses ke View $\rightarrow$ View melakukan pengalihan (*redirect*) ke halaman daftar portofolio dan merender daftar kartu proyek terunggah pada antarmuka Mahasiswa.
2.  **Sequence Diagram - Evaluasi Portofolio Proyek (`evaluasi_portofolio.xml`):**
    *   *Aktor:* Admin/Pembimbing.
    *   *Alur:* Admin mengakses halaman evaluasi portofolio `admin_portofolio.html` $\rightarrow$ Mengirim GET request ke `AdminPortfolioView` $\rightarrow$ View meminta daftar portofolio dari `Portfolio Model` $\rightarrow$ Model melakukan query ke MySQL Database $\rightarrow$ Database mengembalikan dataset portofolio peserta magang $\rightarrow$ View merender halaman evaluasi berisi daftar portofolio $\rightarrow$ Admin memasukkan catatan ulasan (*feedback*) dan mengubah status persetujuan $\rightarrow$ Kirim POST request evaluasi $\rightarrow$ View memperbarui status pada `Portfolio Model` $\rightarrow$ Model menyimpan perubahan di database $\rightarrow$ Database mengonfirmasi sukses $\rightarrow$ View memuat ulang halaman admin secara dinamis dengan status portofolio yang diperbarui.
3.  **Sequence Diagram - Pengelolaan Tugas (`pengelolaan_tugas.xml`):**
    *   *Aktor:* Admin/Pembimbing.
    *   *Alur:* Admin mengisi data penugasan di `admin_tambah_tugas.html` $\rightarrow$ Mengirim POST request ke `TugasCreateView` $\rightarrow$ View menginstansiasi objek `Tugas` $\rightarrow$ Model menyimpan rekam tugas ke database MySQL $\rightarrow$ Database membalas konfirmasi sukses $\rightarrow$ View mengarahkan kembali ke halaman penugasan utama dan memicu notifikasi otomatis ke dasbor mahasiswa yang bersangkutan.

---

## 6. Rancangan Struktur Data & Kamus Data (*Data Dictionary*)

Berdasarkan implementasi model Django di database MySQL, berikut rancangan tabel lengkap sistem SIM-MPP:

### 1. Tabel: `accounts_customuser` (Model: `CustomUser`)
*Deskripsi:* Menyimpan data akun pengguna utama (Mahasiswa & Admin) terintegrasi dengan Firebase UID.

| Nama Kolom | Tipe Data | Kunci | Keterangan / Batasan |
| :--- | :--- | :--- | :--- |
| `id` | INT | Primary Key | Auto Increment |
| `username` | VARCHAR(150) | Unique | Nama pengguna untuk login (diisi email) |
| `email` | VARCHAR(254) | Unique | Alamat email terdaftar |
| `password` | VARCHAR(128) | - | Hash kata sandi pengguna |
| `firebase_uid` | VARCHAR(128) | Unique, Nullable | UID sinkronisasi Firebase Authentication |
| `role` | VARCHAR(10) | - | Pilihan peran: `ADMIN` atau `MAHASISWA` |
| `is_mahasiswa` | BOOLEAN | - | Flag peran Mahasiswa (default: False) |
| `is_admin_pembimbing` | BOOLEAN | - | Flag peran Admin Pembimbing (default: False) |
| `avatar` | VARCHAR(100) | Nullable | Path file foto profil (folder `avatars/`) |
| `nim` | VARCHAR(20) | Nullable | Nomor Induk Mahasiswa |
| `nip` | VARCHAR(30) | Nullable | Nomor Induk Pegawai (khusus Admin) |
| `universitas_id`| INT | Foreign Key | Relasi ke `accounts_masteruniversitas` |
| `jurusan_id` | INT | Foreign Key | Relasi ke `accounts_masterjurusan` |
| `no_telp` | VARCHAR(20) | Nullable | Nomor telepon aktif |
| `tempat_lahir` | VARCHAR(100) | Nullable | Tempat lahir peserta magang |
| `tanggal_lahir` | DATE | Nullable | Tanggal lahir peserta magang |
| `jenis_kelamin` | VARCHAR(1) | Nullable | Pilihan jenis kelamin: `L` atau `P` |
| `unit_kerja` | VARCHAR(200) | Nullable | Unit kerja instansi (khusus Admin) |
| `jabatan` | VARCHAR(100) | Nullable | Jabatan struktural (khusus Admin) |
| `banner_color` | VARCHAR(20) | Nullable | Kode warna preferensi banner visual dashboard |
| `wajib_ganti_sandi`| BOOLEAN | - | Flag pembaruan password wajib (default: True) |
| `is_deleted` | BOOLEAN | - | Flag soft delete akun (default: False) |

### 2. Tabel: `accounts_masteruniversitas` (Model: `MasterUniversitas`)
*Deskripsi:* Menyimpan daftar universitas/perguruan tinggi asal peserta magang.

| Nama Kolom | Tipe Data | Kunci | Keterangan / Batasan |
| :--- | :--- | :--- | :--- |
| `id` | INT | Primary Key | Auto Increment |
| `nama` | VARCHAR(200) | Unique | Nama lengkap universitas |
| `kode_kemendikbud`| VARCHAR(50) | Unique, Nullable | Kode resmi universitas dari Kemendikbud |
| `alamat` | TEXT | Nullable | Alamat fisik universitas |
| `is_aktif` | BOOLEAN | - | Status aktif universitas (default: True) |

### 3. Tabel: `accounts_masterjurusan` (Model: `MasterJurusan`)
*Deskripsi:* Menyimpan daftar program studi / jurusan asal peserta magang.

| Nama Kolom | Tipe Data | Kunci | Keterangan / Batasan |
| :--- | :--- | :--- | :--- |
| `id` | INT | Primary Key | Auto Increment |
| `nama` | VARCHAR(150) | Unique | Nama program studi / jurusan |
| `kode_jurusan` | VARCHAR(50) | Unique, Nullable | Kode identifikasi program studi |

### 4. Tabel: `accounts_profil` (Model: `Profil`)
*Deskripsi:* Menyimpan detail data registrasi tambahan untuk peserta magang (relasi 1:1 ke User).

| Nama Kolom | Tipe Data | Kunci | Keterangan / Batasan |
| :--- | :--- | :--- | :--- |
| `id` | INT | Primary Key | Auto Increment |
| `user_id` | INT | Foreign Key (1:1)| Relasi unik ke `accounts_customuser` |
| `nik` | VARCHAR(30) | Unique | Nomor Induk Kependudukan (KTP) |
| `asal_kampus_id`| INT | Foreign Key | Relasi ke `accounts_masteruniversitas` (PROTECT)|

### 5. Tabel: `logbook_logbook` (Model: `Logbook`)
*Deskripsi:* Menyimpan catatan logbook harian kinerja mahasiswa magang.

| Nama Kolom | Tipe Data | Kunci | Keterangan / Batasan |
| :--- | :--- | :--- | :--- |
| `id` | INT | Primary Key | Auto Increment |
| `user_id` | INT | Foreign Key | Relasi ke mahasiswa pembuat di `accounts_customuser` |
| `tanggal` | DATE | - | Tanggal pelaksanaan kegiatan |
| `judul` | VARCHAR(255) | - | Topik / Nama Kegiatan harian |
| `detail_pekerjaan`| TEXT | - | Deskripsi detail uraian pekerjaan |
| `tautan_pendukung`| VARCHAR(500) | Nullable | URL tautan hasil kerja (Drive/Github) |
| `lampiran_gambar`| VARCHAR(100) | Nullable | Path gambar dokumentasi (`logbook/images/`) |
| `lampiran_dokumen`| VARCHAR(100) | Nullable | Path file dokumen pdf/word (`logbook/docs/`) |
| `keterangan` | VARCHAR(20) | - | Pilihan kehadiran: `HADIR`, `IZIN_PERKULIAHAN`, `WFH` |
| `status` | VARCHAR(10) | - | Status review: `MENUNGGU`, `REVISI`, `DISETUJUI` |
| `catatan_pembimbing`| TEXT | Nullable | Pesan koreksi/umpan balik dari pembimbing |
| `keterangan_file`| VARCHAR(255) | Nullable | Deskripsi singkat dari file pembimbing |
| `file_pembimbing`| VARCHAR(100) | Nullable | Berkas lampiran koreksi dari admin (`logbook/pembimbing/`) |
| `created_at` | DATETIME | - | Stempel waktu pembuatan record (auto) |

### 6. Tabel: `logbook_tugas` (Model: `Tugas`)
*Deskripsi:* Menyimpan daftar tugas terstruktur yang diberikan oleh admin pembimbing kepada mahasiswa.

| Nama Kolom | Tipe Data | Kunci | Keterangan / Batasan |
| :--- | :--- | :--- | :--- |
| `id` | INT | Primary Key | Auto Increment |
| `mahasiswa_id` | INT | Foreign Key | Relasi ke mahasiswa penerima di `accounts_customuser` |
| `judul_tugas` | VARCHAR(255) | - | Judul tugas |
| `deskripsi_tugas`| TEXT | - | Deskripsi deskriptif instruksi tugas |
| `pembimbing` | VARCHAR(255) | - | Nama pembimbing pemberi tugas |
| `deadline` | DATE | - | Batas akhir waktu pengumpulan |
| `status` | VARCHAR(10) | - | Status pengerjaan tugas: `PENDING` atau `SELESAI` |

### 7. Tabel: `portfolio_masterkategori` (Model: `MasterKategori`)
*Deskripsi:* Menyimpan pengelompokan jenis portofolio (misalnya: Web App, Mobile App, UI/UX, dll).

| Nama Kolom | Tipe Data | Kunci | Keterangan / Batasan |
| :--- | :--- | :--- | :--- |
| `id` | INT | Primary Key | Auto Increment |
| `nama` | VARCHAR(100) | Unique | Nama kategori portofolio |
| `slug` | VARCHAR(100) | Unique | Slug URL untuk filtering halaman |

### 8. Tabel: `portfolio_portfolio` (Model: `Portfolio`)
*Deskripsi:* Menyimpan portofolio karya proyek yang dikembangkan mahasiswa selama magang.

| Nama Kolom | Tipe Data | Kunci | Keterangan / Batasan |
| :--- | :--- | :--- | :--- |
| `id` | INT | Primary Key | Auto Increment |
| `user_id` | INT | Foreign Key | Relasi ke mahasiswa pemilik di `accounts_customuser` |
| `judul_proyek` | VARCHAR(255) | - | Nama proyek aplikasi |
| `kategori_id` | INT | Foreign Key | Relasi ke `portfolio_masterkategori` (PROTECT) |
| `teknologi` | VARCHAR(255) | - | Framework/Bahasa pemrograman (React, Node, dll) |
| `database` | VARCHAR(255) | Nullable | Mesin basis data yang digunakan (MySQL, Postgres, dll) |
| `deskripsi` | TEXT | - | Uraian fitur dan fungsionalitas proyek |
| `gambar_sampul` | VARCHAR(100) | - | Path file gambar mockup/tangkapan layar (`portfolio/covers/`) |
| `tautan_repository`| VARCHAR(200) | Nullable | Link repositori kode (GitHub/GitLab) |
| `created_at` | DATETIME | - | Stempel waktu pembuatan record (auto) |

### 9. Tabel: `documents_sertifikat` (Model: `Sertifikat`)
*Deskripsi:* Menyimpan data sertifikat kelulusan magang mahasiswa.

| Nama Kolom | Tipe Data | Kunci | Keterangan / Batasan |
| :--- | :--- | :--- | :--- |
| `id` | INT | Primary Key | Auto Increment |
| `user_id` | INT | Foreign Key (1:1)| Relasi unik ke `accounts_customuser` |
| `file_sertifikat` | VARCHAR(100) | - | Path berkas pdf dokumen sertifikat (`certificates/`) |
| `nomor_sertifikat`| VARCHAR(100) | Unique | Nomor surat keputusan/sertifikat resmi |
| `tanggal_terbit` | DATE | - | Tanggal terbit sertifikat (auto_now_add) |
| `is_verified` | BOOLEAN | - | Status verifikasi sertifikat (default: False) |

### 10. Tabel: `accounts_logaktivitas` / `admin_panel_catatansistem` (Model: `LogAktivitas` / `CatatanSistem`)
*Deskripsi:* Merekam catatan log aktivitas (*audit log*) penting untuk keamanan dan pengawasan sistem.

| Nama Kolom | Tipe Data | Kunci | Keterangan / Batasan |
| :--- | :--- | :--- | :--- |
| `id` | INT | Primary Key | Auto Increment |
| `waktu` | DATETIME | - | Stempel waktu terjadinya aksi |
| `aktor_id` / `user_id`| INT | Foreign Key | Relasi ke `accounts_customuser` (SET_NULL, Nullable) |
| `aktivitas` | VARCHAR(255) / TEXT| - | Deskripsi lengkap tindakan yang dilakukan |
| `tipe` | VARCHAR(20) | - | Jenis operasi: `CREATE`, `UPDATE`, `DELETE`, `LOGIN`, `SYSTEM` |
