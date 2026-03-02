from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import UserForm, UserProfileForm  # Vamos criar esses formulários em seguida

def is_admin(user):
    """Verifica se o usuário é administrador."""
    return user.is_staff or user.is_superuser

@login_required
def profile_view(request):
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
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            messages.success(request, f'Usuário {user.username} criado com sucesso!')
            return redirect('accounts:user_list')
    else:
        user_form = UserForm()

    return render(request, 'accounts/user_form.html', {
        'user_form': user_form,
        'title': 'Criar Usuário',
    })

@login_required
@user_passes_test(is_admin)
def user_update(request, pk):
    """Atualiza um usuário existente (apenas para administradores)."""
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            if user_form.cleaned_data['password']:
                user.set_password(user_form.cleaned_data['password'])
            user.save()
            messages.success(request, f'Usuário {user.username} atualizado com sucesso!')
            return redirect('accounts:user_list')
    else:
        user_form = UserForm(instance=user)

    return render(request, 'accounts/user_form.html', {
        'user_form': user_form,
        'title': 'Editar Usuário',
    })

@login_required
@user_passes_test(is_admin)
def user_delete(request, pk):
    """Exclui um usuário (apenas para administradores)."""
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Usuário {username} excluído com sucesso!')
        return redirect('accounts:user_list')

    return render(request, 'accounts/user_confirm_delete.html', {'user': user})