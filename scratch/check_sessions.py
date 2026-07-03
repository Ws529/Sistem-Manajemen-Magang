import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sim_magang_portofolio.settings')
import django
django.setup()

from django.contrib.sessions.models import Session
from django.utils import timezone
from accounts.models import CustomUser

sessions = Session.objects.filter(expire_date__gte=timezone.now())
print(f"Active sessions: {sessions.count()}")
for s in sessions:
    data = s.get_decoded()
    user_id = data.get('_auth_user_id')
    if user_id:
        try:
            user = CustomUser.objects.get(id=user_id)
            print(f"Session key: {s.session_key}, User: {user.username}, Role: {user.role}, Expire: {s.expire_date}")
        except CustomUser.DoesNotExist:
            print(f"Session key: {s.session_key}, User ID: {user_id} (not found)")
    else:
        print(f"Session key: {s.session_key}, Anonymous session")
