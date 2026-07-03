import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sim_magang_portofolio.settings')
django.setup()

from logbook.models import Logbook

logbooks = Logbook.objects.all().order_by('-tanggal')[:15]
print(f"Total logbooks: {Logbook.objects.count()}")
for l in logbooks:
    print(f"ID: {l.id}, User: {l.user.username}, Tanggal: {l.tanggal}, Judul: {l.judul}, Keterangan: {l.keterangan}, Status: {l.status}")
