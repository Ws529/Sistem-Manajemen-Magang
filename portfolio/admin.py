from django.contrib import admin
from .models import Portfolio, MasterKategori


@admin.register(MasterKategori)
class MasterKategoriAdmin(admin.ModelAdmin):
    list_display = ('nama', 'slug')
    search_fields = ('nama', 'slug')
    prepopulated_fields = {'slug': ('nama',)}


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('judul_proyek', 'user', 'kategori', 'teknologi', 'created_at')
    list_filter = ('kategori',)
    search_fields = ('judul_proyek', 'user__username', 'teknologi')