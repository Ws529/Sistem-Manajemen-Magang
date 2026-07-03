from django.db import models
from django.conf import settings


class CatatanSistem(models.Model):
    """
    Model log aktivitas untuk halaman admin_catatan_sistem.html.
    Merekam setiap aksi penting di dalam sistem (CREATE, UPDATE, DELETE, SYSTEM).
    Kolom tabel: WAKTU · AKTOR / USER · AKTIVITAS · TIPE
    """
    TIPE_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('SYSTEM', 'System'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='catatan_sistem',
        verbose_name='Aktor / User',
    )
    aktivitas = models.TextField(verbose_name='Deskripsi Aktivitas')
    tipe = models.CharField(max_length=10, choices=TIPE_CHOICES, default='SYSTEM', verbose_name='Tipe')
    waktu = models.DateTimeField(auto_now_add=True, verbose_name='Waktu')

    class Meta:
        ordering = ['-waktu']
        verbose_name = 'Catatan Sistem'
        verbose_name_plural = 'Catatan Sistem'

    def __str__(self):
        aktor = self.user.get_full_name() if self.user else 'System'
        return f"[{self.tipe}] {aktor} — {self.aktivitas[:60]}"
