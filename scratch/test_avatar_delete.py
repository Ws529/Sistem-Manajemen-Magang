import os
import sys
from django.core.files.uploadedfile import SimpleUploadedFile

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sim_magang_portofolio.settings')

import django
django.setup()

from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from accounts.models import CustomUser
from accounts.views import profile_view
from admin_panel.views import admin_pengaturan

def test_admin_avatar_delete():
    print("--- Testing Admin Avatar Delete ---")
    admin_user = CustomUser.objects.get(email='admin77011@gmail.com')
    
    # 1. Give the admin a dummy avatar if not set
    dummy_image = SimpleUploadedFile("test_avatar.png", b"file_content", content_type="image/png")
    admin_user.avatar = dummy_image
    admin_user.save()
    admin_user.refresh_from_db()
    
    print(f"Initial avatar path: {admin_user.avatar.name if admin_user.avatar else 'None'}")
    assert admin_user.avatar, "Admin avatar should be set initially"
    
    # 2. Simulate POST request to admin_pengaturan with delete_avatar='true'
    factory = RequestFactory()
    request = factory.post('/admin-panel/pengaturan/', {
        'nama': 'Vallencia',
        'nip': '19850623 202405 1 001',
        'unit_kerja': 'Diskominfosantik Bekasi',
        'jabatan': 'Kepala Bidang',
        'no_telp': '081134567881',
        'email': 'admin77011@gmail.com',
        'delete_avatar': 'true'
    })
    request.user = admin_user
    
    # Add messages framework support
    setattr(request, 'session', {})
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)
    
    # Run the view
    response = admin_pengaturan(request)
    print(f"Response status code: {response.status_code}")
    
    # Refresh user
    admin_user.refresh_from_db()
    print(f"Avatar after deletion: {admin_user.avatar.name if admin_user.avatar else 'None'}")
    assert not admin_user.avatar, "Admin avatar should be deleted"
    print("Admin avatar delete test passed successfully!\n")

def test_user_avatar_delete():
    print("--- Testing User Avatar Delete ---")
    user = CustomUser.objects.get(email='fadzar19@gmail.com')
    
    # 1. Give the user a dummy avatar
    dummy_image = SimpleUploadedFile("test_user_avatar.png", b"file_content", content_type="image/png")
    user.avatar = dummy_image
    user.save()
    user.refresh_from_db()
    
    print(f"Initial avatar path: {user.avatar.name if user.avatar else 'None'}")
    assert user.avatar, "User avatar should be set initially"
    
    # 2. Simulate POST request to profile_view with delete_avatar='true'
    factory = RequestFactory()
    request = factory.post('/user-peserta-magang/profile/', {
        'nama': 'Fadzar',
        'nim': '12345',
        'universitas': 'Unikom',
        'jurusan': 'IF',
        'no_telp': '08123456789',
        'delete_avatar': 'true'
    })
    request.user = user
    
    # Add messages framework support
    setattr(request, 'session', {})
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)
    
    # Run the view
    response = profile_view(request)
    print(f"Response status code: {response.status_code}")
    
    # Refresh user
    user.refresh_from_db()
    print(f"Avatar after deletion: {user.avatar.name if user.avatar else 'None'}")
    assert not user.avatar, "User avatar should be deleted"
    print("User avatar delete test passed successfully!\n")

if __name__ == '__main__':
    test_admin_avatar_delete()
    test_user_avatar_delete()
