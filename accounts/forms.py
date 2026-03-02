from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    """Formulário para criação e edição de usuários."""
    password = forms.CharField(widget=forms.PasswordInput(), required=False, 
                              help_text='Deixe em branco para manter a senha atual')
    is_staff = forms.BooleanField(label='Acesso total', required=False,
                                 help_text='Se marcado, o usuário terá acesso a todas as funcionalidades')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_staff', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Torna os campos opcionais para edição
        if self.instance.pk:
            self.fields['username'].help_text = ''

class UserProfileForm(forms.ModelForm):
    """Formulário para perfil de usuário (para expansão futura)."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']