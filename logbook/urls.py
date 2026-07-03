from django.urls import path
from . import views

urlpatterns = [
    path('tugas/', views.daftar_tugas, name='daftar_tugas'),
    path('entri/', views.entri_logbook, name='entri_logbook'),
    path('riwayat/', views.riwayat_logbook_peserta, name='riwayat_logbook'),
    path('ekspor/word/', views.ekspor_logbook_word, name='ekspor_logbook_word'),
]
