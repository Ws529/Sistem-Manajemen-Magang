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
    help = "Delete a user account given email and password, and clean up Firebase if linked."

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email of the user to delete')
        parser.add_argument('password', type=str, help='Password of the user (for verification)')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise CommandError(f'User with email {email} does not exist.')

        if not user.check_password(password):
            raise CommandError('Password verification failed. Aborting deletion.')

        # Perform deletion inside a transaction
        with transaction.atomic():
            # Delete from Firebase if uid present
            if getattr(user, 'firebase_uid', None) and firebase_auth:
                try:
                    firebase_auth.delete_user(user.firebase_uid)
                    logger.info(f'Firebase user {user.firebase_uid} deleted for {email}.')
                except Exception as e:
                    logger.warning(f'Failed to delete Firebase user for {email}: {e}')
            # Delete the Django user (cascades to related models via on_delete)
            user.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted user {email}.'))
