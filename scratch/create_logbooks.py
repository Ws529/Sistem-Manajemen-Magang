import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sim_magang_portofolio.settings')
import django
django.setup()

from logbook.models import Logbook
from accounts.models import CustomUser

user = CustomUser.objects.get(username='fadzar19@gmail.com')

# Logbook 1: 4 Juni 2026
lb1, created1 = Logbook.objects.get_or_create(
    user=user,
    tanggal=datetime.date(2026, 6, 4),
    defaults={
        'judul': 'Membuat rancangan database',
        'detail_pekerjaan': 'Merancang skema database relasional untuk sistem informasi magang.',
        'keterangan': 'HADIR',
        'status': 'MENUNGGU'
    }
)

# Logbook 2: 5 Juni 2026
lb2, created2 = Logbook.objects.get_or_create(
    user=user,
    tanggal=datetime.date(2026, 6, 5),
    defaults={
        'judul': 'Membuat diagram use case',
        'detail_pekerjaan': 'Membuat dokumentasi diagram use case dan perancangan Entity-Relationship Diagram (ERD).',
        'keterangan': 'HADIR',
        'status': 'MENUNGGU'
    }
)

print(f"Logbook 4 Juni 2026: {'Created' if created1 else 'Already Exists'} (ID: {lb1.id})")
print(f"Logbook 5 Juni 2026: {'Created' if created2 else 'Already Exists'} (ID: {lb2.id})")
