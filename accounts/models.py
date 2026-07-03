from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class MasterUniversitas(models.Model):
    nama = models.CharField(max_length=200, unique=True, verbose_name="Nama Universitas")
    kode_kemendikbud = models.CharField(max_length=50, blank=True, null=True, unique=True)
    alamat = models.TextField(blank=True, null=True)
    is_aktif = models.BooleanField(default=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "Master Universitas"
        verbose_name_plural = "Master Universitas"


class MasterJurusan(models.Model):
    nama = models.CharField(max_length=150, unique=True, verbose_name="Nama Jurusan")
    kode_jurusan = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "Master Jurusan"
        verbose_name_plural = "Master Jurusan"


class CustomUser(AbstractUser):
    firebase_uid = models.CharField(max_length=128, unique=True, null=True, blank=True)
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MAHASISWA', 'Mahasiswa'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MAHASISWA')

    is_mahasiswa = models.BooleanField(default=False)
    is_admin_pembimbing = models.BooleanField(default=False)

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    nim = models.CharField(max_length=20, blank=True, null=True)
    universitas = models.ForeignKey(MasterUniversitas, on_delete=models.SET_NULL, blank=True, null=True)
    no_telp = models.CharField(max_length=20, blank=True, null=True)
    jurusan = models.ForeignKey(MasterJurusan, on_delete=models.SET_NULL, blank=True, null=True)

    # ── Field tambahan dari user_profile.html ────────────────────
    JENIS_KELAMIN_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]
    tempat_lahir = models.CharField(max_length=100, blank=True, null=True, verbose_name='Tempat Lahir')
    tanggal_lahir = models.DateField(blank=True, null=True, verbose_name='Tanggal Lahir')
    jenis_kelamin = models.CharField(
        max_length=1,
        choices=JENIS_KELAMIN_CHOICES,
        blank=True,
        null=True,
        verbose_name='Jenis Kelamin',
    )

    # ── Field admin dari admin_pengaturan.html ───────────────────
    nip = models.CharField(max_length=30, blank=True, null=True, verbose_name='NIP')
    unit_kerja = models.CharField(max_length=200, blank=True, null=True, verbose_name='Unit Kerja')
    jabatan = models.CharField(max_length=100, blank=True, null=True, verbose_name='Jabatan')

    # Simpan preferensi warna banner
    banner_color = models.CharField(max_length=20, blank=True, null=True)

    wajib_ganti_sandi = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    # Menghindari konflik dengan field bawaan
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True,
    )

    class Meta:
        verbose_name = 'Pengguna'
        verbose_name_plural = 'Pengguna'

    def __str__(self):
        return self.get_full_name() or self.username


class Profil(models.Model):
    user = models.OneToOneField(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='profil',
    )
    nik = models.CharField(max_length=30, unique=True, verbose_name='NIK')
    asal_kampus = models.ForeignKey(MasterUniversitas, on_delete=models.PROTECT, verbose_name='Asal Kampus')

    class Meta:
        verbose_name = 'Profil Peserta'
        verbose_name_plural = 'Profil Peserta'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} — {self.nik}"

class LogAktivitas(models.Model):
    TIPE_CHOICES = (
        ('CREATE', 'CREATE'),
        ('UPDATE', 'UPDATE'),
        ('DELETE', 'DELETE'),
        ('SYSTEM', 'SYSTEM'),
        ('LOGIN', 'LOGIN'),
    )
    waktu = models.DateTimeField(auto_now_add=True)
    aktor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    aktivitas = models.CharField(max_length=255)
    tipe = models.CharField(max_length=20, choices=TIPE_CHOICES)

    class Meta:
        ordering = ['-waktu']

    def __str__(self):
        return f"[{self.waktu}] {self.aktor} - {self.aktivitas}"