import os
import sys
import django

# Add the parent directory of scratch to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sim_magang_portofolio.settings')
django.setup()

from accounts.models import CustomUser

users = CustomUser.objects.all()
print(f"Total users: {users.count()}")
for u in users:
    print(f"ID: {u.id}, Username: {u.username}, Role: {u.role}, Email: {u.email}, Full Name: {u.get_full_name()}, IsMahasiswa: {u.is_mahasiswa}")
