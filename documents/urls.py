from django.urls import path
from . import views

urlpatterns = [
    path('', views.daftar_dokumen, name='daftar_dokumen'),
    path('support/', views.support_view, name='support'),
]
