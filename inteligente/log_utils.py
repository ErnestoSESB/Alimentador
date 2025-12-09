"""
Utilitários para registrar logs de atividades do sistema
"""
from .models import ActivityLog


def get_client_ip(request):
    """Obtém o endereço IP do cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_activity(user, action, description, feeder=None, request=None):
    """
    Registra uma atividade no sistema
    
    Args:
        user: Usuário que executou a ação (pode ser None para ações do sistema)
        action: Tipo de ação ('create', 'update', 'delete', 'login', 'logout', etc.)
        description: Descrição detalhada da ação
        feeder: Alimentador relacionado (opcional)
        request: Request HTTP para capturar IP (opcional)
    """
    ip_address = None
    if request:
        ip_address = get_client_ip(request)
    
    return ActivityLog.objects.create(
        user=user,
        feeder=feeder,
        action=action,
        description=description,
        ip_address=ip_address
    )


def log_feeder_action(user, feeder, action, description, request=None):
    """Registra uma ação relacionada a um alimentador"""
    return log_activity(user, action, description, feeder=feeder, request=request)


def log_user_action(user, action, description, request=None):
    """Registra uma ação do usuário (login, logout, etc)"""
    return log_activity(user, action, description, request=request)
