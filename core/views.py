from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
import datetime

@login_required
def dashboard(request):
    """Exibe o dashboard principal."""
    # Por enquanto, apenas renderiza o template
    return render(request, 'core/dashboard/dashboard.html')

@login_required
def transaction_list(request):
    """Lista todas as transações."""
    # Por enquanto, apenas renderiza o template
    return render(request, 'core/transactions/transaction_list.html')

@login_required
def transaction_create(request):
    """Cria uma nova transação."""
    # Por enquanto, apenas renderiza o template
    return render(request, 'core/transactions/transaction_form.html')

@login_required
def transaction_detail(request, pk):
    """Exibe detalhes de uma transação."""
    # Por enquanto, apenas renderiza o template
    return render(request, 'core/transactions/transaction_detail.html')

@login_required
def transaction_update(request, pk):
    """Atualiza uma transação existente."""
    # Por enquanto, apenas renderiza o template
    return render(request, 'core/transactions/transaction_form.html')

@login_required
def transaction_delete(request, pk):
    """Exclui uma transação."""
    # Por enquanto, apenas renderiza o template
    return render(request, 'core/transactions/transaction_confirm_delete.html')

@login_required
def category_list(request):
    """Lista todas as categorias."""
    # Por enquanto, apenas renderiza o template
    return render(request, 'core/categories/category_list.html')

@login_required
def category_create(request):
    """Cria uma nova categoria."""
    # Por enquanto, apenas renderiza o template
    return render(request, 'core/categories/category_form.html')

@login_required
def category_update(request, pk):
    """Atualiza uma categoria existente."""
    # Por enquanto, apenas renderiza o template
    return render(request, 'core/categories/category_form.html')

@login_required
def category_delete(request, pk):
    """Exclui uma categoria."""
    # Por enquanto, apenas renderiza o template
    return render(request, 'core/categories/category_confirm_delete.html')

@login_required
def report(request):
    """Exibe relatórios financeiros."""
    # Por enquanto, apenas renderiza o template
    return render(request, 'core/reports/report.html')

@login_required
def import_transactions(request):
    """Importa transações de um arquivo XLSX."""
    # Por enquanto, apenas renderiza o template
    return render(request, 'core/import/import.html')