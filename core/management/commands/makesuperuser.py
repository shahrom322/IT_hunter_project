from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создает польлзователя с уникальными правами'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                "admin", "admin@domain.com", "admin")
            self.stdout.write(
                self.style.SUCCESS('Супер пользователь был успешно создан. Логин: admin, Пароль: admin')
            )
        else:
            self.stdout.write(self.style.ERROR('Супер пользователь уже существует'))
