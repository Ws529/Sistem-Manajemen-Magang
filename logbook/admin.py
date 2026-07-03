from django.contrib import admin
from .models import Logbook, Tugas


@admin.register(Logbook)
class LogbookAdmin(admin.ModelAdmin):
    list_display = ('user', 'tanggal', 'judul', 'status', 'keterangan')
    list_filter = ('status', 'keterangan', 'tanggal')
    search_fields = ('user__username', 'judul', 'detail_pekerjaan')
    date_hierarchy = 'tanggal'


@admin.register(Tugas)
class TugasAdmin(admin.ModelAdmin):
    list_display = ('judul_tugas', 'mahasiswa', 'deadline', 'status')
    list_filter = ('status', 'deadline')
    search_fields = ('judul_tugas', 'mahasiswa__username', 'deskripsi_tugas')