from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "inteligente/index.html")

def farmer_template(request):
    return render(request, "inteligente/farmer_template")

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import Feeder, Alert, UserProfile
from django.shortcuts import render
from django.db.models import Avg
from inteligente.models import Feeder, Alert
from inteligente.forms import feederForm, Feeder


def login_view(request):
    """Login view"""
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        userobject = User.objects.get(email=email)
        user = authenticate(request, username=userobject.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Email ou senha inválidos.')
    
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
    return render(request, 'feeders/detail.html', {'feeder': feeder})
    

@login_required
def feeder_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        owner = request.POST.get('owner')
        capacity = request.POST.get('capacity')
        status = request.POST.get('status')
        food_level = request.POST.get('food_level')
        daily_consumption = request.POST.get('daily_consumption')
        last_maintenance = request.POST.get('last_maintenance')
        next_maintenance = request.POST.get('next_maintenance')

        feeder = Feeder.objects.create(
            name=name,
            location=location,
            owner=owner,
            capacity=capacity,
            status=status,
            food_level=food_level,
            daily_consumption=daily_consumption,
            last_maintenance=last_maintenance,
            next_maintenance=next_maintenance
        )

    
        messages.success(request, f'Alimentador "{name}" adicionado com sucesso!')
        return redirect('feeders') 

    return render(request, 'feeders/add.html')

@login_required
def feeder_edit(request, feeder_id):

    feeder = get_object_or_404(Feeder, id=feeder_id)

    if request.method == 'POST':
        form = feederForm(request.POST, instance=feeder)
        if form.is_valid():
            form.save()
            messages.success(request, f'Alimentador "{feeder.name}" atualizado com sucesso!')
            return redirect('feeder_detail', feeder_id=feeder.id)
        else:
            messages.error(request, 'Erro ao atualizar o alimentador. Verifique os dados e tente novamente.')
    else:
        form = feederForm(instance=feeder)

    return render(request, 'feeders/edit.html', {'form': form, 'feeder': feeder})

@login_required
def users_list(request):
    
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
def user_detail(request, user_id):
    """User detail view"""
    user = get_object_or_404(User, id=user_id)
    
    # Get user's feeders if they are a farmer
    feeders = []
    if hasattr(user, 'profile') and user.profile.role == 'farmer':
        feeders = Feeder.objects.filter(owner=user.get_full_name())
    
    context = {
        'user_obj': user,  # Avoid conflict with request.user
        'feeders': feeders,
    }
    
    return render(request, 'users/detail.html', context)

@login_required
def user_add(request):
    """Add new user"""
    if request.method == 'POST':
        # Handle form submission
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        phone = request.POST.get('phone')
        
        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password='temp123'  # Temporary password
        )
        
        # Create profile
        UserProfile.objects.create(
            user=user,
            role=role,
            phone=phone
        )
        
        messages.success(request, f'Usuário "{user.get_full_name()}" adicionado com sucesso!')
        return redirect('user_detail', user_id=user.id)
    
    return render(request, 'users/add.html')

@login_required
def user_edit(request, user_id):
    """Edit user"""
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        # Handle form submission
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        
        # Update profile
        if hasattr(user, 'profile'):
            user.profile.role = request.POST.get('role')
            user.profile.phone = request.POST.get('phone')
            user.profile.save()
        
        messages.success(request, f'Usuário "{user.get_full_name()}" atualizado com sucesso!')
        return redirect('user_detail', user_id=user.id)
    
    context = {
        'user_obj': user,
    }
    
    return render(request, 'users/edit.html', context)

@login_required
def alerts_list(request):
    """Alerts list view with filtering"""
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
def reports_index(request):

    top_qs = Feeder.objects.order_by('-daily_consumption')

    report_data = {
        'feeding_efficiency': 94,
        'total_consumption': 1250,
        'average_level': 65,
        'system_uptime': 99.2,
        'maintenance_completed': 8,
        'alerts_generated': 12,
    }
    # Top feeders data
    top_feeders = [
        {'name': 'Alimentador Pasto Norte', 'consumption': 380, 'efficiency': 96},
        {'name': 'Alimentador Central', 'consumption': 450, 'efficiency': 94},
        {'name': 'Alimentador Pasto Sul', 'consumption': 320, 'efficiency': 92},
    ]
    
    context = {
        'report_data': report_data,
        'top_feeders': top_feeders,
    }
    
    return render(request, 'reports/index.html', context)

@login_required
def dashboard(request):

    total_feeders = Feeder.objects.count()
    active_feeders = Feeder.objects.filter(status='active')
    inactive_feeders = total_feeders - active_feeders.count()
    alerts_count = Alert.objects.filter(resolved=False).count()
    average_food_level = Feeder.objects.aggregate(Avg('food_level'))['food_level__avg'] or 0

    recent_alerts = Alert.objects.filter(resolved=False).order_by('-created_at')[:3]

    context = {
        'stats': {
            'total_feeders': total_feeders,
            'active_feeders': active_feeders.count(),
            'inactive_feeders': inactive_feeders,
            'alerts_count': alerts_count,
            'average_food_level': round(average_food_level),
        },
        'recent_alerts': recent_alerts,
        'active_feeders': active_feeders[:4],  # exibe apenas os primeiros 4 ativos
    }

    return render(request, 'dashboard/index.html', context)