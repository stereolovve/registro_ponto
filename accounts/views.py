from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile


def login_view(request):
    """Session-based login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciais inválidas')

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """Logout view"""
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Logout realizado com sucesso')
        return redirect('login')
    return redirect('dashboard')


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        # Validações
        if not all([username, email, password, password2]):
            messages.error(request, 'Todos os campos são obrigatórios')
        elif password != password2:
            messages.error(request, 'As senhas não coincidem')
        elif len(password) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'E-mail já cadastrado')
        else:
            # Criar usuário
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Profile é criado automaticamente via signal
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('dashboard')

    return render(request, 'accounts/register.html')


@login_required
def perfil_view(request):
    """View user profile"""
    return render(request, 'accounts/perfil.html')


@login_required
def perfil_editar_view(request):
    """Edit user profile"""
    if request.method == 'POST':
        profile = request.user.profile

        # Campos editáveis
        valor_hora = request.POST.get('valor_hora')
        departamento = request.POST.get('departamento', '')
        telefone = request.POST.get('telefone', '')

        try:
            profile.valor_hora = valor_hora
            profile.departamento = departamento
            profile.telefone = telefone
            profile.save()

            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('perfil')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar perfil: {str(e)}')

    return render(request, 'accounts/perfil_editar.html')
