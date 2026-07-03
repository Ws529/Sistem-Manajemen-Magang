from django.contrib import admin
from .models import Sertifikat


@admin.register(Sertifikat)
class SertifikatAdmin(admin.ModelAdmin):
    list_display = ('user', 'nomor_sertifikat', 'tanggal_terbit', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('user__username', 'nomor_sertifikat')
