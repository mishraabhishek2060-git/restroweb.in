import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create the initial admin account from deployment environment variables.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_ADMIN_USERNAME', 'restaurantadmin')
        password = os.environ.get('DJANGO_ADMIN_PASSWORD')
        email = os.environ.get('DJANGO_ADMIN_EMAIL', '')
        if not password:
            raise CommandError('Set DJANGO_ADMIN_PASSWORD before creating the deployment admin.')

        user_model = get_user_model()
        if user_model.objects.filter(username=username).exists():
            self.stdout.write(f'Admin account {username!r} already exists.')
            return

        user_model.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Created deployment admin account {username!r}.'))

