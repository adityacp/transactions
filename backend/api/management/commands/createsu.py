from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from api.models import Account


class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password='Python321'
            )
        print('Superuser has been created.')
        try:
            for i in range(1, 11):
                entry = "test_user"+str(i)
                u = User.objects.create_user(username=entry, password=entry, first_name=entry, last_name=entry)
                Account.objects.create(user=u, balance=10000)
        except Exception:
            pass
