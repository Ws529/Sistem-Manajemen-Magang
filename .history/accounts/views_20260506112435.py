from django.shortcuts import render
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
import json

def dashboard(request):
    return render(request, 'dashboard.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
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