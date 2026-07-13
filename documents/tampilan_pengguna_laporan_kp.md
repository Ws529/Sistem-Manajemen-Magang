# SUB-BAB 3.11: TAMPILAN PENGGUNA (USER INTERFACE)

Tampilan Pengguna atau *User Interface* (UI) merupakan jembatan interaksi antara pengguna (*user*) dengan fungsionalitas sistem. Desain antarmuka **Sistem Informasi Manajemen Magang & Portofolio Proyek (SIM-MPP)** ini dibangun dengan menerapkan prinsip *User Experience* (UX) yang berfokus pada kemudahan penggunaan (*usability*), efisiensi alur kerja (*user flow*), serta konsistensi visual.

Secara teknis, perancangan antarmuka pada sistem SIM-MPP diimplementasikan dengan mempertimbangkan beberapa aspek utama sebagai berikut:
1. **Responsivitas Antarmuka (*Responsive Web Design*):** Layout dirancang secara fleksibel menggunakan kombinasi CSS Grid dan Flexbox. Hal ini memastikan seluruh halaman sistem dapat diakses secara optimal baik melalui perangkat komputer (*desktop*), tablet, maupun telepon genggam (*mobile screen*) tanpa merusak struktur tata letak menu.
2. **Kustomisasi Visual & Estetika Modern:** Sistem mendukung personalisasi visual, salah satunya melalui fitur kustomisasi warna banner atas (*banner color*) dan pemotongan foto profil lingkaran (*circular cropper*) berasio 1:1. Penyesuaian preferensi estetika ini membantu meminimalisasi kejenuhan pengguna saat berinteraksi dengan sistem setiap hari.
3. **Kejelasan Status dan Feedback Sistem:** Untuk setiap aksi penting (seperti penyimpanan data, kesalahan input format gambar, atau penghapusan berkas), sistem menyediakan visualisasi umpan balik yang informatif. Salah satu contohnya adalah tombol **Hapus Foto** yang secara dinamis memperbarui pratinjau menjadi gambar inisial nama secara instan untuk menegaskan status perubahan data sebelum disimpan ke database.

Melalui pendekatan ini, antarmuka SIM-MPP diharapkan dapat mempercepat proses adaptasi pengguna—baik mahasiswa magang dalam melakukan pencatatan logbook maupun pembimbing lapangan dalam melakukan validasi aktivitas dan evaluasi tugas secara harian.

---

## 3.11.1 Antarmuka Autentikasi (Halaman Login)

Sistem menyediakan dua pintu masuk terpisah untuk menjaga keamanan akses dan memisahkan hak otorisasi pengguna:

1.  **Halaman Login Peserta Magang (Mahasiswa):**
    *   *Fungsi:* Digunakan oleh mahasiswa magang aktif untuk masuk menggunakan alamat email dan kata sandi yang telah terdaftar.
    *   *Elemen UI:* Kolom input email, kolom input kata sandi, tombol masuk terintegrasi dengan verifikasi reCAPTCHA v3/Firebase App Check untuk mencegah serangan *brute force*, serta tautan pemulihan kata sandi (*Lupa Password*).
2.  **Halaman Login Administrator (Pembimbing):**
    *   *Fungsi:* Portal khusus pembimbing lapangan dan superadmin untuk mengelola sistem.
    *   *Elemen UI:* Desain minimalis yang senada dengan login mahasiswa tetapi diarahkan ke *endpoint* otorisasi staf/admin, dilengkapi proteksi otentikasi ganda yang sinkron dengan Firebase Auth.

---

## 3.11.2 Antarmuka Dasbor Utama (Dashboard)

Halaman dasbor dirancang berbeda menyesuaikan dengan peran (*role*) aktor yang masuk:

1.  **Dasbor Mahasiswa:**
    *   *Deskripsi:* Menampilkan ringkasan progres magang secara visual, meliputi statistik logbook disetujui, tugas yang harus diselesaikan, dan modul pengumuman.
    *   *Elemen UI:* Kartu metrik (*Metric Cards*) dengan ikon dinamis, daftar tugas aktif berurutan berdasarkan tanggal batas waktu (*deadline*), dan status keaktifan peserta.
2.  **Dasbor Administrator:**
    *   *Deskripsi:* Menyediakan ringkasan cepat aktivitas seluruh peserta magang untuk mempermudah pemantauan harian.
    *   *Elemen UI:* Tiga kartu statistik utama (*Total Peserta Magang*, *Antrean Validasi Logbook*, *Tugas Tertunda*), grafik/tabel ringkas mahasiswa aktif, serta umpan aktivitas logbook terbaru yang masuk ke dalam sistem.

---

## 3.11.3 Antarmuka Profil & Pengaturan Pengguna

Halaman ini berfungsi sebagai pusat kontrol profil pengguna dan admin untuk memelihara data personal serta preferensi tampilan dasbor:

1.  **Banner Kustomisasi Latar Belakang (*Banner Color Customizer*):**
    *   *Fitur:* Fitur interaktif di mana pengguna dapat memilih warna banner atas menggunakan *color picker* bawaan. Warna yang dipilih akan langsung diterapkan secara *real-time* di frontend dan disimpan ke database menggunakan AJAX.
2.  **Modul Sesuaikan Foto Profil (*Circular Image Cropper*):**
    *   *Fitur:* Menggunakan pustaka *Cropper.js* untuk memungkinkan pengguna memotong foto profil yang diunggah ke dalam bentuk lingkaran rasio 1:1 sebelum disimpan ke server, memastikan foto profil pas dan proporsional.
3.  **Fitur Hapus Foto Profil & Fallback Inisial Nama:**
    *   *Fitur Baru:* Tombol **Hapus Foto** (dengan ikon *trash* merah) disediakan untuk membuang foto profil dari database dan menghapus berkas fisiknya dari server secara permanen.
    *   *Visualisasi:* Ketika pengguna menekan tombol hapus, antarmuka frontend secara instan memperbarui pratinjau gambar profil menjadi inisial nama pengguna (misalnya: "VL" untuk Vallencia) menggunakan API eksternal `ui-avatars.com` dengan latar belakang warna dinamis sesuai role (biru sky untuk user, gelap untuk admin).

---

## 3.11.4 Antarmuka Manajemen Logbook (Aktivitas Harian)

Modul ini memfasilitasi pencatatan kegiatan harian mahasiswa magang:

1.  **Formulir Input Logbook (Mahasiswa):**
    *   *Elemen UI:* Kolom tanggal kegiatan, pilihan kategori kehadiran (*HADIR*, *IZIN_PERKULIAHAN*, *WFH*), input uraian detail pekerjaan, kolom tautan pendukung (GitHub/Drive), dan tombol unggah berkas (gambar dokumentasi dan dokumen PDF).
2.  **Halaman Riwayat Logbook & Ekspor Word (Mahasiswa):**
    *   *Elemen UI:* Daftar tabel riwayat logbook lengkap dengan filter status (*MENUNGGU*, *REVISI*, *DISETUJUI*). Disediakan tombol **Ekspor Logbook** untuk mengunduh rekap riwayat logbook langsung ke format Microsoft Word (`.docx`).
3.  **Halaman Validasi Logbook (Admin):**
    *   *Elemen UI:* Tabel antrean peninjauan logbook. Admin dapat mengklik baris data untuk membuka modul detail logbook mahasiswa, mengisi kolom umpan balik/catatan pembimbing, melampirkan berkas koreksi, dan memberikan keputusan persetujuan.

---

## 3.11.5 Antarmuka Pengelolaan Tugas (Penugasan)

Modul integrasi antara instruksi pembimbing dan pengerjaan mahasiswa:

1.  **Halaman Penugasan Admin:**
    *   *Elemen UI:* Formulir pemberian tugas baru (dropdown nama mahasiswa, judul, instruksi pengerjaan, dan tanggal batas waktu). Di bawahnya terdapat tabel daftar tugas yang sudah diberikan lengkap dengan status pengerjaan mahasiswa.
2.  **Halaman Daftar Tugas Mahasiswa:**
    *   *Elemen UI:* Menampilkan daftar tugas terstruktur dari pembimbing. Mahasiswa dapat menandai tugas yang telah selesai dikerjakan, yang kemudian akan memicu perubahan status tugas di dasbor admin.

---

## 3.11.6 Antarmuka Portofolio Proyek Magang

Galeri pameran hasil karya aplikasi yang dibangun oleh peserta magang:

1.  **Formulir Tambah Portofolio (Mahasiswa):**
    *   *Elemen UI:* Input judul proyek, kategori proyek (Dropdown berbasis *MasterKategori*), daftar teknologi/framework yang digunakan, database pendukung, uraian fitur proyek, unggah gambar tangkapan layar/mockup aplikasi, serta tautan repositori kode.
2.  **Halaman Galeri Portofolio (Admin & Mahasiswa):**
    *   *Elemen UI:* Kartu proyek (*Project Cards*) yang rapi dengan visual mockup, kategori proyek, dan tombol detail. Admin dapat memantau, memfilter portofolio berdasarkan teknologi atau kategori, dan menghapus portofolio yang tidak valid.

---

## 3.11.7 Antarmuka Laporan Performa & Catatan Sistem (Admin)

Modul pengawasan teknis dan administratif bagi pembimbing:

1.  **Halaman Rekapitulasi Laporan Performa:**
    *   *Elemen UI:* Tabel analisis performa mahasiswa magang (menghitung jumlah logbook disetujui dan rasio penyelesaian tugas). Disediakan tombol **Ekspor Laporan** ke dalam format file `.csv` yang ramah Microsoft Excel.
2.  **Halaman Catatan Sistem (Audit Log):**
    *   *Elemen UI:* Daftar riwayat aksi sistem terperinci yang mencatat kejadian (waktu, aktor, detail aktivitas, dan tipe aksi seperti `CREATE`, `UPDATE`, `DELETE`, `LOGIN`, `SYSTEM`) untuk memantau keamanan dan mendeteksi kesalahan input data.
