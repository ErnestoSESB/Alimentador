from .models import Alert

def alerts_count(request):

    if request.user.is_authenticated:
        from .views import is_admin_user
        
        if is_admin_user(request.user):
 
            count = Alert.objects.filter(resolved=False).count()
        else:
      
            user_full_name = request.user.get_full_name() or request.user.username
            count = Alert.objects.filter(
                feeder__owner=user_full_name,
                resolved=False
            ).count()
        
        return {'alerts_count': count}
    
    return {'alerts_count': 0}