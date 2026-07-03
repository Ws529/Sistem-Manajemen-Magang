from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
import json

def dashboard(request):
    return render(request, 'dashboard.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        nama_lengkap = request.POST.get('nama_lengkap', '').strip()
        nim = request.POST.get('nim', '').strip()
        universitas = request.POST.get('universitas', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        form_data = {
            'nama_lengkap': nama_lengkap,
            'nim': nim,
            'universitas': universitas,
            'email': email,
        }

        if password != password_confirm:
            messages.error(request, 'Password dan konfirmasi password tidak cocok.')
            return render(request, 'register.html', {'form_data': form_data})

        if len(password) < 8:
            messages.error(request, 'Password minimal 8 karakter.')
            return render(request, 'register.html', {'form_data': form_data})

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah terdaftar. Gunakan email lain.')
            return render(request, 'register.html', {'form_data': form_data})

        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=nama_lengkap,
            role='MAHASISWA',
        )
        messages.success(request, 'Akun berhasil dibuat. Silakan masuk.')
        return redirect('login')

    return render(request, 'register.html')

@csrf_exempt
def sync_firebase_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            uid = data.get('uid')
            email = data.get('email')
            role = data.get('role', 'MAHASISWA')

            user, created = CustomUser.objects.get_or_create(
                firebase_uid=uid,
                defaults={'email': email, 'username': email, 'role': role}
            )

            if not created:
                user.email = email
                if 'role' in data:
                    user.role = data.get('role')
                user.save()

            login(request, user)
            return JsonResponse({'status': 'success', 'role': user.role})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)