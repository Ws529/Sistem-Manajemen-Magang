from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('data-mahasiswa/', views.admin_data_mahasiswa, name='admin_data_mahasiswa'),
    path('catatan-sistem/', views.admin_catatan_sistem, name='admin_catatan_sistem'),
    path('logbook-peserta/', views.admin_logbook, name='admin_logbook'),
    path('portofolio/', views.admin_portofolio, name='admin_portofolio'),
    path('penugasan/', views.admin_penugasan, name='admin_penugasan'),
    path('sertifikat/', views.admin_sertifikat, name='admin_sertifikat'),
    path('export-mahasiswa/', views.export_mahasiswa_csv, name='export_mahasiswa_csv'),
    path('laporan/', views.admin_laporan, name='admin_laporan'),
    path('laporan/export/', views.export_laporan_excel, name='export_laporan_excel'),
    path('portofolio/export/', views.export_portfolio_excel, name='export_portfolio_excel'),
    path('pengaturan/', views.admin_pengaturan, name='admin_pengaturan'),
]
