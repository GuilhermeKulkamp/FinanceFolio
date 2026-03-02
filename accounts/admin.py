from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_access_level')

    def get_access_level(self, obj):
        return obj.profile.get_access_level_display()
    get_access_level.short_description = 'Nível de Acesso'

# Re-registrar o modelo User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)