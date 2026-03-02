from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """
    Modelo para armazenar informações adicionais do usuário.
    """
    ACCESS_CHOICES = (
        ('total', 'Acesso Total'),
        ('partial', 'Acesso Parcial'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    access_level = models.CharField(max_length=10, choices=ACCESS_CHOICES, default='partial')

    def __str__(self):
        return f"{self.user.username} - {self.get_access_level_display()}"

    @property
    def is_admin(self):
        """Verifica se o usuário é administrador."""
        return self.user.is_staff or self.user.is_superuser

    @property
    def has_total_access(self):
        """Verifica se o usuário tem acesso total."""
        return self.access_level == 'total' or self.is_admin

# alterado para tornar o código mais simples e evitar erros de importação circular
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#    """Cria um perfil de usuário quando um novo usuário é criado."""
#    if created:
#        UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#    """Salva o perfil de usuário quando o usuário é salvo."""
#    instance.profile.save()