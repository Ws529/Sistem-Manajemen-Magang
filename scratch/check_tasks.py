import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sim_magang_portofolio.settings')
import django
django.setup()

from logbook.models import Tugas
from accounts.models import CustomUser

user = CustomUser.objects.get(username='fadzar19@gmail.com')
tasks = Tugas.objects.filter(mahasiswa=user)
print(f"Tasks for {user.username}: {tasks.count()}")
for t in tasks:
    print(f"ID: {t.id}, Judul: {t.judul_tugas}, Deskripsi: {t.deskripsi_tugas}, Deadline: {t.deadline}, Status: {t.status}")
