from django.db import models
from django.conf import settings


class Logbook(models.Model):
    STATUS_CHOICES = [
        ('MENUNGGU', 'Menunggu'),
        ('REVISI', 'Revisi'),
        ('DISETUJUI', 'Disetujui'),
    ]

    KETERANGAN_CHOICES = [
        ('HADIR', 'Hadir'),
        ('IZIN_PERKULIAHAN', 'Izin Perkuliahan'),
        ('WFH', 'WFH'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tanggal = models.DateField()
    judul = models.CharField(max_length=255, default='Logbook Harian')
    detail_pekerjaan = models.TextField(verbose_name='Uraian')
    tautan_pendukung = models.URLField(max_length=500, blank=True, null=True)
    lampiran_gambar = models.ImageField(upload_to='logbook/images/', blank=True, null=True)
    lampiran_dokumen = models.FileField(upload_to='logbook/docs/', blank=True, null=True)
    keterangan = models.CharField(max_length=20, choices=KETERANGAN_CHOICES, default='HADIR')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='MENUNGGU')
    catatan_pembimbing = models.TextField(blank=True, null=True)
    keterangan_file = models.CharField(max_length=255, blank=True, null=True, default='')
    file_pembimbing = models.FileField(upload_to='logbook/pembimbing/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.tanggal}"

    class Meta:
        ordering = ['-tanggal']
        verbose_name = 'Logbook'
        verbose_name_plural = 'Logbook'


class Tugas(models.Model):
    STATUS_TUGAS = [
        ('PENDING', 'Pending'),
        ('SELESAI', 'Selesai'),
    ]

    mahasiswa = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tugas_mahasiswa',
    )
    judul_tugas = models.CharField(max_length=255, verbose_name='Judul')
    deskripsi_tugas = models.TextField(blank=True, verbose_name='Deskripsi')
    pembimbing = models.CharField(max_length=255)
    deadline = models.DateField(verbose_name='Batas Waktu')
    status = models.CharField(max_length=10, choices=STATUS_TUGAS, default='PENDING')

    def __str__(self):
        return self.judul_tugas

    class Meta:
        verbose_name = 'Tugas'
        verbose_name_plural = 'Tugas'