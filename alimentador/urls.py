"""
URL configuration for alimentador project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inteligente.views import farmer_template, index
from inteligente import views

urlpatterns = [
    
    #path('farmer/', farmer_template),
    #path('', index),
]
# Django URLs for AgroFeeder System
from django.urls import path
from inteligente import views

urlpatterns = [
    # Authentication
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Feeders
    path('feeders/', views.feeders_list, name='feeders'),
    path('feeders/add/', views.feeder_add, name='feeder_add'),
    path('feeders/<int:feeder_id>/edit/', views.feeder_edit, name='feeder_edit'),
    path('feeders/<int:feeder_id>/', views.feeder_detail, name='feeder_detail'),
    # Users
    path('users/', views.users_list, name='users'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    
    # Alerts
    path('alerts/', views.alerts_list, name='alerts'),
    path('alerts/<int:alert_id>/resolve/', views.alert_resolve, name='alert_resolve'),
    path('alerts/<int:alert_id>/dismiss/', views.alert_dismiss, name='alert_dismiss'),
    
    # Reports
    path('reports/', views.reports_index, name='reports'),
]