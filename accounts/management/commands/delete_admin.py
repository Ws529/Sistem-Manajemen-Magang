from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db import transaction
import logging

# Attempt to import firebase admin if available
try:
    from firebase_admin import auth as firebase_auth
except Exception:  # pragma: no cover
    firebase_auth = None

User = get_user_model()
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Delete an admin user by full name (first and last name). Also removes linked Firebase account if any."

    def add_arguments(self, parser):
        parser.add_argument('first_name', type=str, help='First name of the admin user')
        parser.add_argument('last_name', type=str, help='Last name of the admin user')

    def handle(self, *args, **options):
        first_name = options['first_name']
        last_name = options['last_name']
        try:
            admin_user = User.objects.get(first_name=first_name, last_name=last_name, role='ADMIN')
        except User.DoesNotExist:
            raise CommandError(f'Admin user {first_name} {last_name} does not exist.')

        # Perform deletion inside a transaction
        with transaction.atomic():
            # Delete from Firebase if uid present
            if getattr(admin_user, 'firebase_uid', None) and firebase_auth:
                try:
                    firebase_auth.delete_user(admin_user.firebase_uid)
                    logger.info(f'Firebase user {admin_user.firebase_uid} deleted for admin {first_name} {last_name}.')
                except Exception as e:
                    logger.warning(f'Failed to delete Firebase user for admin {first_name} {last_name}: {e}')
            # Delete the admin user (cascades to related models via on_delete)
            admin_user.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted admin user {first_name} {last_name}.'))
