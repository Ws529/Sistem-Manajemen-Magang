from django.db import models
from django.conf import settings


class MasterKategori(models.Model):
    nama = models.CharField(max_length=100, unique=True, verbose_name="Nama Kategori")
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "Master Kategori"
        verbose_name_plural = "Master Kategori"


class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    judul_proyek = models.CharField(max_length=255, verbose_name='Judul')
    kategori = models.ForeignKey(MasterKategori, on_delete=models.PROTECT, verbose_name='Kategori')
    teknologi = models.CharField(max_length=255)  # Contoh: React & Node.js
    database = models.CharField(max_length=255, blank=True, null=True, verbose_name='Database')
    deskripsi = models.TextField()
    gambar_sampul = models.ImageField(upload_to='portfolio/covers/')
    tautan_repository = models.URLField(blank=True, null=True, verbose_name='Tautan / File Proyek')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul_proyek

    class Meta:
        verbose_name = 'Portofolio'
        verbose_name_plural = 'Portofolio'
