from django.db import models
from django.conf import settings


class Sertifikat(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_sertifikat = models.FileField(upload_to='certificates/', verbose_name='File Dokumen')
    nomor_sertifikat = models.CharField(max_length=100, unique=True)
    tanggal_terbit = models.DateField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Sertifikat - {self.user.username}"

    class Meta:
        verbose_name = 'Sertifikat'
        verbose_name_plural = 'Sertifikat'