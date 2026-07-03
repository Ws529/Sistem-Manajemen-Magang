from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.contrib import messages

class AuthenticationSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        
        # Tentukan area terproteksi
        is_user_area = path.startswith('/user-peserta-magang/')
        is_admin_area = path.startswith('/admin-panel/')
        
        if is_user_area or is_admin_area:
            # 1. CEK AUTENTIKASI: Jika belum login, alihkan ke login yang sesuai
            if not request.user.is_authenticated:
                # Hindari looping jika mengakses rute publik di bawah path ini (jika ada)
                # Di proyek ini, rute masuk berada di /accounts/login/ sehingga aman.
                if is_admin_area:
                    return redirect(f"{reverse('login_admin')}?next={path}")
                else:
                    return redirect(f"{reverse('login')}?next={path}")
            
            # 2. OTORISASI PERAN (ROLE ENFORCEMENT)
            user = request.user
            
            # Mahasiswa dilarang keras mengakses Halaman Admin
            if is_admin_area and not (user.is_staff or user.role == 'ADMIN' or user.is_superuser):
                return HttpResponseForbidden(
                    '<h1>403 – Akses Ditolak</h1>'
                    '<p>Halaman ini dilindungi secara ketat dan hanya untuk Administrator SIM-MPP. '
                    '<a href="/">Kembali ke Dasbor Anda</a></p>'
                )
                
            # Admin dilarang mengakses Halaman Mahasiswa (alihkan ke admin dashboard)
            if is_user_area and (user.is_staff or user.role == 'ADMIN' or user.is_superuser):
                return redirect('/admin-panel/dashboard/')

        response = self.get_response(request)
        
        # 3. KEAMANAN CACHE: Cegah browser menyimpan cache halaman dasbor privat
        # Ini memastikan jika user klik tombol "Kembali (Back)" di browser setelah logout,
        # mereka akan dipaksa login ulang oleh server alih-alih melihat cache halaman usang.
        if is_user_area or is_admin_area:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            
        return response
