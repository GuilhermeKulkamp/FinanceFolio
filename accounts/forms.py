from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import UserProfile

class UserForm(forms.ModelForm):
    """Formulário para edição de usuários."""
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Sobrenome')
    email = forms.EmailField(max_length=254, required=True, label='E-mail')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    """Formulário para edição do perfil de usuário."""
    class Meta:
        model = UserProfile
        fields = ('access_level',)
        labels = {
            'access_level': 'Nível de Acesso',
        }
        widgets = {
            'access_level': forms.Select(attrs={'class': 'form-select'}),
        }

class UserRegistrationForm(UserCreationForm):
    """Formulário para registro de novos usuários."""
    first_name = forms.CharField(max_length=30, required=True, label='Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Sobrenome')
    email = forms.EmailField(max_length=254, required=True, label='E-mail')
    is_staff = forms.BooleanField(required=False, label='Administrador', 
                                 help_text='Permite acesso ao painel de administração')
    access_level = forms.ChoiceField(
        choices=UserProfile.ACCESS_CHOICES,
        required=True,
        label='Nível de Acesso',
        initial='partial',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'access_level')

class CustomPasswordChangeForm(PasswordChangeForm):
    """Formulário personalizado para alteração de senha."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})