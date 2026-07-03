from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_peserta_page, name='login'),
    path('login/peserta/', views.login_peserta_page, name='login_peserta'),
    path('login/admin/', views.login_admin_page, name='login_admin'),
    path('register/peserta/', views.register_peserta_page, name='register_peserta'),
    path('register/admin/', views.register_admin_page, name='register_admin'),
    path('logout/', views.logout_view, name='logout'),
    path('api/login/peserta/', views.api_login_peserta, name='api_login_peserta'),
    path('api/login/admin/', views.api_login_admin, name='api_login_admin'),
    path('sync-firebase/', views.sync_firebase_user, name='sync_firebase_user'),
    path('update-banner-color/', views.update_banner_color, name='update_banner_color'),
    path('ubah-sandi-wajib/', views.halaman_ubah_sandi_wajib, name='halaman_ubah_sandi_wajib'),
    path('lupa-password/', views.lupa_password_view, name='lupa_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password_view, name='reset_password'),
]
