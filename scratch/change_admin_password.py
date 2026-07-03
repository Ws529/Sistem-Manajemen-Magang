import os
import sys
import django

# Add the parent directory of scratch to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sim_magang_portofolio.settings')
django.setup()

from accounts.models import CustomUser
from accounts.views import _sync_to_firebase
from firebase_admin import auth as firebase_auth

email = "admin77011@gmail.com"
new_password = "admin123"

try:
    user = CustomUser.objects.get(email=email)
    # Update Django locally
    user.set_password(new_password)
    user.save()
    print(f"Password updated successfully for {email} in local Django database.")
    
    # Sync with Firebase
    if user.firebase_uid:
        try:
            firebase_auth.update_user(user.firebase_uid, password=new_password)
            print(f"Password synchronized to Firebase Auth for UID: {user.firebase_uid}")
        except Exception as e:
            print(f"Warning: Failed to update password in Firebase Auth directly: {e}")
            print("Attempting helper synchronization...")
            try:
                _sync_to_firebase(user, password=new_password)
                print("Firebase helper synchronization succeeded.")
            except Exception as e2:
                print(f"Error: Sync to Firebase failed completely: {e2}")
    else:
        try:
            _sync_to_firebase(user, password=new_password)
            print("Firebase helper synchronization succeeded (created new Firebase account).")
        except Exception as e:
            print(f"Error: Failed to sync user to Firebase: {e}")

except CustomUser.DoesNotExist:
    print(f"Error: User with email {email} does not exist.")
except Exception as e:
    print(f"Error: {e}")
