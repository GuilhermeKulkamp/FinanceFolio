from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Cria perfis de usuário para usuários existentes'

    def handle(self, *args, **options):
        users_without_profile = []
        for user in User.objects.all():
            try:
                profile = user.profile
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=user)
                users_without_profile.append(user.username)

        if users_without_profile:
            self.stdout.write(self.style.SUCCESS(f'Perfis criados para: {", ".join(users_without_profile)}'))
        else:
            self.stdout.write(self.style.SUCCESS('Todos os usuários já possuem perfil'))