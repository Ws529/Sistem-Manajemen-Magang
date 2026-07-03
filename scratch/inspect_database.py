import os
import django
import datetime
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sim_magang_portofolio.settings')
django.setup()

from logbook.models import Logbook

# Wait for DB connection
for i in range(10):
    try:
        count = Logbook.objects.count()
        print("Successfully connected to MySQL database!")
        break
    except Exception as e:
        print(f"Waiting for database... ({i+1}/10) Error: {e}")
        time.sleep(2)
else:
    print("Could not connect to database after 10 attempts.")
    exit(1)

print("=== TOTAL LOGBOOK IN DATABASE ===")
print("Total entries:", Logbook.objects.count())

print("\n=== RECENT LOGBOOK ENTRIES (TOP 5) ===")
for l in Logbook.objects.order_by('-tanggal')[:5]:
    print(f"ID: {l.id} | Tanggal: {l.tanggal} | User: {l.user.username}")
    print(f"Judul: {l.judul}")
    print(f"Uraian: {l.detail_pekerjaan}")
    print(f"Status: {l.status} | Keterangan: {l.keterangan}")
    print("-" * 50)

print("\n=== TODAY'S LOGBOOK ENTRIES (2026-05-29) ===")
today = datetime.date(2026, 5, 29)
todays_entries = Logbook.objects.filter(tanggal=today)
print(f"Found {todays_entries.count()} entries:")
for l in todays_entries:
    print(f"ID: {l.id} | User: {l.user.username}")
    print(f"Judul: {l.judul}")
    print(f"Uraian: {l.detail_pekerjaan}")
    print("-" * 50)
