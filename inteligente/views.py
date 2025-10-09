from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Feeder, Alert, User, UserProfile
from .forms import feederForm, FarmerFeederForm, alertForm, FarmerAlertForm, Feeder, User, UserForm, UserProfile, UserProfileForm, FarmerProfileForm
import re

# Helper function to check admin permissions
def is_admin_user(user):
    """Check if user has admin permissions"""
    if user.is_superuser:
        return True
    user_profile = getattr(user, 'profile', None)
    return user_profile and user_profile.role == 'admin'
def landing_page(request):
    return render(request, "alimentador/alimentador.html")
# Create your views here.
def index(request):
    return render(request, "inteligente/index.html")

def farmer_template(request):
    return render(request, "inteligente/farmer_template")

def login_view(request):
    """Login view"""
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        users = User.objects.filter(email=email)
        if not users.exists():
            messages.error(request, "Usuário não encontrado.")
            return redirect('login')

        user = users.first()
        if user.check_password(password): 
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Senha incorreta.")
            return redirect('login')

    return render(request, 'auth/login.html')
def logout_view(request):
    """Logout view"""
    logout(request)
    return redirect('login')

'''@login_required
def dashboard(request):
    """Dashboard view with statistics"""
    # Get statistics
    total_feeders = Feeder.objects.count()
    active_feeders = Feeder.objects.filter(status='active')
    pending_alerts = Alert.objects.filter(resolved=False)
    
    stats = {


@login_required
def alert_edit(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id)
    if request.method == 'POST':
        alert.type = request.POST.get('type')
        alert.message = request.POST.get('message')
        alert.severity = request.POST.get('severity')
        alert.resolved = bool(request.POST.get('resolved'))
        alert.save()
        messages.success(request, 'Alerta atualizado com sucesso!')
        return redirect('alerts')
    context = {
        'alert': alert,
    }
    return render(request, 'alerts/edit.html', context)
        'total_feeders': total_feeders,
        'active_feeders': active_feeders.count(),
        'inactive_feeders': total_feeders - active_feeders.count(),
        'alerts_count': pending_alerts.count(),
        'average_food_level': 40  # Calculate from actual data
    }
    
    # Recent alerts (last 3)
    recent_alerts = pending_alerts.order_by('-created_at')[:3]
    
    # Active feeders for status display
    active_feeders_list = active_feeders[:4]
    
    context = {
        'stats': stats,
        'recent_alerts': recent_alerts,
        'active_feeders': active_feeders_list,
        'alerts_count': pending_alerts.count(),
    }
    
    return render(request, 'dashboard/index.html', context)
'''
@login_required
def feeders_list(request):
    user_profile = getattr(request.user, 'profile', None)
    
    # Filter feeders based on user role
    if user_profile and user_profile.role == 'farmer':
        # Farmers see only their own feeders
        user_full_name = request.user.get_full_name() or request.user.username
        feeders = Feeder.objects.filter(owner=user_full_name)
    else:
        # Admins see all feeders
        feeders = Feeder.objects.all()
    
    search = request.GET.get('search')
    if search:
        feeders = feeders.filter(
            Q(name__icontains=search) |
            Q(location__icontains=search) |
            Q(owner__icontains=search)
        )
    
    status = request.GET.get('status')
    if status:
        feeders = feeders.filter(status=status)
    paginator = Paginator(feeders, 12) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'feeders': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    
    return render(request, 'feeders/list.html', context)

@login_required
def feeder_detail(request, feeder_id):
    feeder = get_object_or_404(Feeder, id=feeder_id)
    
    # Check permissions for farmers
    user_profile = getattr(request.user, 'profile', None)
    if user_profile and user_profile.role == 'farmer':
        user_full_name = request.user.get_full_name() or request.user.username
        if feeder.owner != user_full_name:
            messages.error(request, 'Você não tem permissão para ver este alimentador.')
            return redirect('feeders')
    
    return render(request, 'feeders/detail.html', {'feeder': feeder})
    

@login_required
def feeder_add(request):
    user_profile = getattr(request.user, 'profile', None)
    is_farmer = user_profile and user_profile.role == 'farmer'
    
    if request.method == 'POST':
        # Use formulário específico baseado no perfil do usuário
        if is_farmer:
            form = FarmerFeederForm(request.POST)
        else:
            form = feederForm(request.POST)
            
        if form.is_valid():
            feeder = form.save(commit=False)
            
            if is_farmer:
                feeder.owner = request.user.get_full_name() or request.user.username
                from django.utils import timezone
                from datetime import timedelta
                feeder.last_maintenance = timezone.now().date()
                feeder.next_maintenance = timezone.now().date() + timedelta(days=30)
            
            # Garantir que next_feeding_time seja definido se não estiver no formulário
            if not hasattr(feeder, 'next_feeding_time') or not feeder.next_feeding_time:
                from django.utils import timezone
                from datetime import timedelta
                feeder.next_feeding_time = timezone.now() + timedelta(hours=8)  # Próxima alimentação em 8 horas
            feeder.save()
            messages.success(request, f'Alimentador "{feeder.name}" adicionado com sucesso!')
            return redirect('feeders')
        else:
            # Add specific error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Erro no campo {field}: {error}')
            messages.error(request, 'Erro ao adicionar o alimentador. Verifique os dados e tente novamente.')
    else:
        # Use formulário específico baseado no perfil do usuário
        if is_farmer:
            form = FarmerFeederForm()
        else:
            form = feederForm()

    context = {
        'form': form,
        'is_farmer': is_farmer,
    }
    return render(request, 'feeders/add.html', context)

@login_required
def feeder_edit(request, feeder_id):
    feeder = get_object_or_404(Feeder, id=feeder_id)
    user_profile = getattr(request.user, 'profile', None)
    is_farmer = user_profile and user_profile.role == 'farmer'
    
    # Check permissions for farmers
    if is_farmer:
        user_full_name = request.user.get_full_name() or request.user.username
        if feeder.owner != user_full_name:
            messages.error(request, 'Você não tem permissão para editar este alimentador.')
            return redirect('feeders')

    if request.method == 'POST':
        # Use formulário específico baseado no perfil do usuário
        if is_farmer:
            form = FarmerFeederForm(request.POST, instance=feeder)
        else:
            form = feederForm(request.POST, instance=feeder)
            
        if form.is_valid():
            feeder_obj = form.save(commit=False)
            
            # Farmers cannot change owner or maintenance dates
            if is_farmer:
                # Preserve original values that farmers shouldn't change
                original_feeder = Feeder.objects.get(id=feeder_id)
                feeder_obj.owner = original_feeder.owner
                feeder_obj.last_maintenance = original_feeder.last_maintenance
                feeder_obj.next_maintenance = original_feeder.next_maintenance
            
            feeder_obj.save()
            messages.success(request, f'Alimentador "{feeder_obj.name}" atualizado com sucesso!')
            return redirect('feeder_detail', feeder_id=feeder_obj.id)
        else:
            messages.error(request, 'Erro ao atualizar o alimentador. Verifique os dados e tente novamente.')
    else:
        # Use formulário específico baseado no perfil do usuário
        if is_farmer:
            form = FarmerFeederForm(instance=feeder)
        else:
            form = feederForm(instance=feeder)

    context = {
        'form': form, 
        'feeder': feeder,
        'is_farmer': is_farmer,
    }
    return render(request, 'feeders/edit.html', context)

@login_required
def users_list(request):
    # Only admins can view users list
    user_profile = getattr(request.user, 'profile', None)
    if user_profile and user_profile.role != 'admin' and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para acessar esta área.')
        return redirect('dashboard')
    
    users = User.objects.all().select_related('profile')

    search = request.GET.get('search')
    if search:
        users = users.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(profile__phone__icontains=search)
        )
    

    role = request.GET.get('role')
    if role:
        users = users.filter(profile__role=role)
    
    # Order users to avoid pagination warning
    users = users.order_by('id')

    paginator = Paginator(users, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'users': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    
    return render(request, 'users/list.html', context)

@login_required
def user_detail(request, user_id, user_name=None):
    # Only admins can view user details
    user_profile = getattr(request.user, 'profile', None)
    if user_profile and user_profile.role != 'admin' and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para acessar esta área.')
        return redirect('dashboard')

    user = get_object_or_404(User, id=user_id)
    
    feeders = []
    if hasattr(user, 'profile') and user.profile.role == 'farmer':
        feeders = Feeder.objects.filter(owner=user.get_full_name())

    user_alerts_count = 0
    if feeders:
        user_alerts_count = Alert.objects.filter(
            feeder_name__in=[f.name for f in feeders]
        ).count()
    
    context = {
        'user_obj': user, 
        'feeders': feeders,
        'user_alerts_count': user_alerts_count,
        'feeders_count': feeders.count() if feeders else 0,
    }
    
    return render(request, 'users/detail.html', context)

@login_required
def user_add(request):
    user_is_admin = False
    
    if request.user.is_superuser:
        user_is_admin = True
    elif hasattr(request.user, 'profile') and request.user.profile.role == 'admin':
        user_is_admin = True
    
    if not user_is_admin:
        messages.error(request, "Apenas administradores podem criar usuários.")
        return redirect('users')

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            try:
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()

        
                role = profile_form.cleaned_data['role']
                group, created = Group.objects.get_or_create(name=role)
                user.groups.add(group)
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.created_by_admin = True
                profile.save()

                messages.success(request, f'Usuário "{user.get_full_name()}" adicionado com sucesso!')
                return redirect('users')
            except Exception as e:
                messages.error(request, f"Erro ao salvar usuário: {str(e)}")
        else:
            messages.error(request, "Erro ao adicionar o usuário. Verifique os dados e tente novamente.")
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'users/add.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def user_delete(request, user_id):
    # Only admins can delete users
    if not is_admin_user(request.user):
        messages.error(request, 'Você não tem permissão para acessar esta área.')
        return redirect('dashboard')
        
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuário excluído com sucesso!')
        return redirect('users')
    return render(request, 'users/confirm_delete.html', {'user_obj': user})
    
@login_required
@login_required
def user_edit(request, user_id, user_name=None):
    """Edit user with robust profile handling"""
    if not is_admin_user(request.user):
        messages.error(request, 'Você não tem permissão para acessar esta área.')
        return redirect('dashboard')
        
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        try:
            from django.db import transaction
            
            with transaction.atomic():
                user.first_name = request.POST.get('first_name', '')
                user.last_name = request.POST.get('last_name', '')
                user.email = request.POST.get('email', '')
                user.save()
                
                role = request.POST.get('role', 'operator')
                phone = request.POST.get('phone', '')
                address = request.POST.get('address', '')
                
                profiles = UserProfile.objects.filter(user=user)
                if profiles.count() > 1:
                    primary_profile = profiles.first()
                    profiles.exclude(id=primary_profile.id).delete()
                    
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'role': role,
                        'phone': phone,
                        'address': address
                    }
                )
                
                if not created:
                    profile.role = role
                    profile.phone = phone
                    profile.address = address
                    profile.save()
            
            messages.success(request, f'Usuário "{user.get_full_name()}" atualizado com sucesso!')
            return redirect('users')
            
        except Exception as e:
            messages.error(request, f'Erro ao salvar usuário: {str(e)}')
    
    context = {
        'user_obj': user,
    }
    
    return render(request, 'users/edit.html', context)

@login_required
def farmer_profile_edit(request):
    """Permite que agricultores editem seu próprio perfil, incluindo resumo executivo"""
    user_profile = getattr(request.user, 'profile', None)
    
    if not user_profile or user_profile.role != 'farmer':
        messages.error(request, 'Acesso negado. Esta funcionalidade é apenas para agricultores.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = FarmerProfileForm(request.POST, instance=user_profile)
        
        # Remove campos obrigatórios de senha para edição
        user_form.fields['password'].required = False
        user_form.fields['confirm_password'].required = False
        
        if user_form.is_valid() and profile_form.is_valid():
            user_data = user_form.cleaned_data
            if not user_data.get('password'):
                user_data.pop('password', None)
                user_data.pop('confirm_password', None)
                
                for field, value in user_data.items():
                    if hasattr(request.user, field):
                        setattr(request.user, field, value)
                request.user.save()
            else:
                request.user.set_password(user_data['password'])
                request.user.save()
            
            profile_form.save()
            
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('farmer_profile_edit')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = FarmerProfileForm(instance=user_profile)
        
        user_form.fields['password'].required = False
        user_form.fields['confirm_password'].required = False
        user_form.fields['password'].widget.attrs['placeholder'] = 'Deixe em branco para não alterar'
        user_form.fields['confirm_password'].widget.attrs['placeholder'] = 'Deixe em branco para não alterar'
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_obj': request.user,
    }
    
    return render(request, 'users/farmer_edit.html', context)

@login_required
def alert_edit(request, alert_id):

    alert = get_object_or_404(Alert, id=alert_id)
    if request.method == 'POST':
        
        Alert.feeder = request.POST.get('feeder')
        Alert.feeder_name = request.POST.get('feeder_name')

@login_required
def alert_delete(request, alert_id):
    alert = get_object_or_404(Alert, id=alert_id)
    if request.method == 'POST':
        alert.delete()
        messages.sucess(request, 'Alerta excluido com sucesso')
        return redirect('alerts')

@login_required
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuário excluído com sucesso!')
        return redirect('users')
    return render(request, 'users/delete_confirm.html', {'user_obj': user})

@login_required
def alerts_list(request):
    """Alerts list view with filtering based on user role"""
    user_profile = getattr(request.user, 'profile', None)
    
    # Filter alerts based on user role
    if user_profile and user_profile.role == 'farmer':
        # Farmers see only alerts from their feeders
        user_full_name = request.user.get_full_name() or request.user.username
        alerts = Alert.objects.filter(feeder__owner=user_full_name).order_by('-created_at')
    else:
        # Admins see all alerts
        alerts = Alert.objects.all().order_by('-created_at')
    
    # Severity filter
    severity = request.GET.get('severity')
    if severity:
        alerts = alerts.filter(severity=severity)
    
    # Type filter
    alert_type = request.GET.get('type')
    if alert_type:
        alerts = alerts.filter(type=alert_type)
    
    # Separate pending and resolved alerts
    pending_alerts = alerts.filter(resolved=False)
    resolved_alerts = alerts.filter(resolved=True)
    
    context = {
        'pending_alerts': pending_alerts,
        'resolved_alerts': resolved_alerts,
        'pending_alerts_count': pending_alerts.count(),
        'resolved_alerts_count': resolved_alerts.count(),
    }
    
    return render(request, 'alerts/list.html', context)

@login_required
@require_POST
def alert_resolve(request, alert_id):
    """Resolve an alert"""
    alert = get_object_or_404(Alert, id=alert_id)
    alert.resolved = True
    alert.save()
    
    messages.success(request, f'Alerta "{alert.message}" foi resolvido.')
    return redirect('alerts')

@login_required
@require_POST
def alert_dismiss(request, alert_id):
    """Dismiss an alert"""
    alert = get_object_or_404(Alert, id=alert_id)
    alert.delete()
    
    messages.success(request, 'Alerta foi descartado.')
    return redirect('alerts')

@login_required
def alert_add(request):
    """Adicionar um novo alerta"""
    user_profile = getattr(request.user, 'profile', None)
    is_farmer = user_profile and user_profile.role == 'farmer'
    
    if request.method == 'POST':
        # Use formulário específico baseado no perfil do usuário
        if is_farmer:
            form = FarmerAlertForm(user=request.user, data=request.POST)
        else:
            form = alertForm(request.POST)
            
        if form.is_valid():
            alert = form.save(commit=False)
            alert.feeder_name = alert.feeder.name
            alert.created_at = timezone.now()
            
            # Verificar se agricultor tem permissão para este alimentador
            if is_farmer:
                user_full_name = request.user.get_full_name() or request.user.username
                if alert.feeder.owner != user_full_name:
                    messages.error(request, 'Você não tem permissão para criar alertas para este alimentador.')
                    return redirect('alerts')
            
            alert.save()
            messages.success(request, f'Alerta adicionado com sucesso para {alert.feeder.name}!')
            return redirect('alerts')
        else:
            messages.error(request, 'Erro ao adicionar o alerta. Verifique os dados e tente novamente.')
    else:
        # Use formulário específico baseado no perfil do usuário
        if is_farmer:
            form = FarmerAlertForm(user=request.user)
        else:
            form = alertForm()

    context = {
        'form': form,
        'is_farmer': is_farmer,
    }
    
    return render(request, 'alerts/add.html', context)

@login_required
def reports_index(request):
    """
    Relatórios com dados específicos por perfil:
    - Agricultores: veem apenas dados dos seus próprios alimentadores
    - Administradores: veem dados de todo o sistema
    """
    user_profile = getattr(request.user, 'profile', None)
    
    # Determinar escopo dos dados baseado no perfil
    if user_profile and user_profile.role == 'farmer':
        user_full_name = request.user.get_full_name() or request.user.username
        feeders = Feeder.objects.filter(owner=user_full_name)
        alerts = Alert.objects.filter(feeder__owner=user_full_name)
        is_farmer = True
        scope_label = f"seus {feeders.count()} alimentadores"
    else:
        feeders = Feeder.objects.all()
        alerts = Alert.objects.all()
        is_farmer = False
        scope_label = f"todos os {feeders.count()} alimentadores do sistema"

    # Calcular métricas baseadas nos dados disponíveis
    total_feeders = feeders.count()
    total_alerts = alerts.count()
    
    if total_feeders > 0:
        base_efficiency = 95 if is_farmer else 92
        efficiency_penalty = min(total_alerts * 2, 15)
        feeding_efficiency = max(base_efficiency - efficiency_penalty, 75)
        
        consumption_per_feeder = 320 if is_farmer else 280
        total_consumption = total_feeders * consumption_per_feeder
        
        from django.db.models import Avg
        avg_level_result = feeders.aggregate(Avg('food_level'))
        average_level = round(avg_level_result['food_level__avg'] or 0)
        
        system_uptime = 99.5 if total_alerts < 3 else 98.2 if total_alerts < 8 else 96.8
        maintenance_completed = max(1, total_feeders // 2)
    else:
        feeding_efficiency = 0
        total_consumption = 0
        average_level = 0
        system_uptime = 100
        maintenance_completed = 0

    report_data = {
        'feeding_efficiency': feeding_efficiency,
        'total_consumption': total_consumption,
        'average_level': average_level,
        'system_uptime': system_uptime,
        'maintenance_completed': maintenance_completed,
        'alerts_generated': total_alerts,
        'total_feeders': total_feeders,
        'scope_label': scope_label,
        'is_farmer': is_farmer,
    }
    
    top_feeders = []
    for i, feeder in enumerate(feeders.order_by('name')[:5]):
        base_consumption = 250 + (i * 50)
        feeder_alerts = alerts.filter(feeder=feeder).count()
        feeder_efficiency = max(95 - (feeder_alerts * 3), 80)
        
        top_feeders.append({
            'name': feeder.name,
            'consumption': base_consumption,
            'efficiency': feeder_efficiency,
            'alerts_count': feeder_alerts,
        })
    
    if not top_feeders and is_farmer:
        context_message = "Você ainda não possui alimentadores cadastrados."
    elif not top_feeders:
        context_message = "Nenhum alimentador cadastrado no sistema."
    else:
        context_message = None
    
    context = {
        'report_data': report_data,
        'top_feeders': top_feeders,
        'context_message': context_message,
        'is_farmer': is_farmer,
        'created_by_admin': user_profile.created_by_admin if user_profile else False,
        'custom_executive_summary': user_profile.custom_executive_summary if user_profile else None,
    }
    
    return render(request, 'reports/index.html', context)

@login_required
def dashboard(request):
    user_profile = getattr(request.user, 'profile', None)
    
    # Filter data based on user role
    if user_profile and user_profile.role == 'farmer':
        # Farmers see only their own feeders and alerts
        user_full_name = request.user.get_full_name() or request.user.username
        feeders = Feeder.objects.filter(owner=user_full_name)
        alerts = Alert.objects.filter(feeder__owner=user_full_name)
    else:
        # Admins see everything
        feeders = Feeder.objects.all()
        alerts = Alert.objects.all()

    total_feeders = feeders.count()
    active_feeders = feeders.filter(status='active')
    inactive_feeders = total_feeders - active_feeders.count()
    alerts_count = alerts.filter(resolved=False).count()
    average_food_level = feeders.aggregate(Avg('food_level'))['food_level__avg'] or 0

    recent_alerts = alerts.filter(resolved=False).order_by('-created_at')[:3]

    context = {
        'stats': {
            'total_feeders': total_feeders,
            'active_feeders': active_feeders.count(),
            'inactive_feeders': inactive_feeders,
            'average_food_level': round(average_food_level),
        },
        'recent_alerts': recent_alerts,
        'active_feeders': active_feeders[:4],  # exibe apenas os primeiros 4 ativos
    }

    return render(request, 'dashboard/index.html', context)