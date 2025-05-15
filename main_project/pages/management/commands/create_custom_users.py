from django.core.management.base import BaseCommand
from pages.models import User, CustomUser


class Command(BaseCommand):
    help = 'Creates CustomUser objects for existing User records'

    def handle(self, *args, **options):
        users = User.objects.all()
        created_count = 0
        
        for user in users:
            if not CustomUser.objects.filter(email=user.email).exists():
                CustomUser.objects.create_user(
                    email=user.email,
                    password=user.password  # Note: This assumes the password is stored as plain text
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created CustomUser for {user.email}'))
        
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} CustomUser objects'))