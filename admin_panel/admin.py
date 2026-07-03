from django.contrib import admin
from .models import CatatanSistem


@admin.register(CatatanSistem)
class CatatanSistemAdmin(admin.ModelAdmin):
    list_display = ('waktu', 'user', 'aktivitas', 'tipe')
    list_filter = ('tipe', 'waktu')
    search_fields = ('aktivitas', 'user__username', 'user__first_name')
    date_hierarchy = 'waktu'
    readonly_fields = ('waktu',)
