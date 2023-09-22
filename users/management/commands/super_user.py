from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        User = get_user_model()

        self.stdout.write('Running migration')
        call_command('migrate')

        self.stdout.write('Creating superuser...')
        username = 'admintest'
        password = 'admin@1234'
        role = 'admin'
        email = 'admintest@admin.com'

        try:
            user = User.objects.create_superuser(
                username=username,
                password=password,
                role=role,
                email=email
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
            self.stdout.write(f'Username: {username}')
            self.stdout.write(f'Password: {password}')
            self.stdout.write(f'Email: {email}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {str(e)}'))
