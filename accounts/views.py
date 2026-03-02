from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse

from .models import UserProfile
from .forms import UserForm, ProfileForm, UserRegistrationForm, CustomPasswordChangeForm

def is_admin(user):
    """Verifica se o usuário é administrador."""
    return user.is_staff or user.is_superuser

@login_required
def profile_view(request):
    # Garantir que o perfil existe
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    """Exibe e permite editar o perfil do usuário logado."""
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('accounts:profile')
    else:
        user_form = UserForm(instance=request.user)

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
    })

@login_required
def change_password(request):
    """Permite ao usuário alterar sua senha."""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def user_list(request):
    """Lista todos os usuários (apenas para administradores)."""
    users = User.objects.all().order_by('username')
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def user_create(request):
    """Cria um novo usuário (apenas para administradores)."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            access_level = form.cleaned_data.get('access_level')
            profile = user.profile
            profile.access_level = access_level
            profile.save()
            messages.success(request, f'Usuário {user.username} criado com sucesso!')
            return redirect('accounts:user_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Criar Usuário'})

@login_required
@user_passes_test(is_admin)
def user_update(request, pk):
    """Atualiza um usuário existente (apenas para administradores)."""
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Usuário {user.username} atualizado com sucesso!')
            return redirect('accounts:user_list')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)

    return render(request, 'accounts/user_update.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_obj': user,
        'title': 'Editar Usuário',
    })

@login_required
@user_passes_test(is_admin)
def user_delete(request, pk):
    """Exclui um usuário (apenas para administradores)."""
    user = get_object_or_404(User, pk=pk)

    # Impedir que o usuário exclua a si mesmo
    if user == request.user:
        messages.error(request, 'Você não pode excluir seu próprio usuário!')
        return redirect('accounts:user_list')

    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Usuário {username} excluído com sucesso!')
        return redirect('accounts:user_list')

    return render(request, 'accounts/user_confirm_delete.html', {'user_obj': user})