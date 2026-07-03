from django.contrib import admin
from .models import CustomUser, Profil, MasterUniversitas, MasterJurusan


@admin.register(MasterUniversitas)
class MasterUniversitasAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kode_kemendikbud', 'is_aktif')
    search_fields = ('nama', 'kode_kemendikbud')


@admin.register(MasterJurusan)
class MasterJurusanAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kode_jurusan')
    search_fields = ('nama', 'kode_jurusan')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'nim', 'universitas', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'jenis_kelamin')
    search_fields = ('username', 'email', 'nim', 'first_name', 'last_name', 'universitas')
    fieldsets = (
        ('Akun', {
            'fields': ('username', 'email', 'password', 'role', 'is_staff', 'is_active',
                        'is_mahasiswa', 'is_admin_pembimbing', 'firebase_uid'),
        }),
        ('Data Personal', {
            'fields': ('first_name', 'last_name', 'avatar', 'tempat_lahir',
                        'tanggal_lahir', 'jenis_kelamin', 'no_telp'),
        }),
        ('Data Akademik / Kepegawaian', {
            'fields': ('nim', 'universitas', 'jurusan', 'nip', 'unit_kerja', 'jabatan'),
        }),
        ('Preferensi', {
            'fields': ('banner_color',),
        }),
    )


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'nik', 'asal_kampus')
    search_fields = ('nik', 'asal_kampus', 'user__username', 'user__first_name')
