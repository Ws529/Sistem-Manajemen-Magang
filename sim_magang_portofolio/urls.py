"""
URL configuration for sim_magang_portofolio project.
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import RedirectView

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/images/logo_kab-bekasi.png')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('captcha/', include('captcha.urls')),

    # Root → Smart redirect berdasarkan status autentikasi
    path('', account_views.root_split_view, name='root_index'),

    # User Dashboard (dedicated path)
    path('user-peserta-magang/dashboard/', account_views.dashboard_view, name='dashboard'),

    # Auth URLs now managed in accounts/urls.py

    # User Panel Pages
    path('user-peserta-magang/profile/', account_views.profile_view, name='profile'),
    path('user-peserta-magang/logbook/', include('logbook.urls')),
    path('user-peserta-magang/portfolio/', include('portfolio.urls')),
    path('user-peserta-magang/dokumen/', include('documents.urls')),

    # Admin Panel
    path('admin-panel/', include('admin_panel.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
