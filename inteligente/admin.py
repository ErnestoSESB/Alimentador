from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Feeder, Alert, MaintenanceLog, FeedingLog


# Inline admin for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Perfil"


# Extend User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "get_role",
        "is_staff",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "profile__role")

    def get_role(self, obj):
        if hasattr(obj, "profile"):
            return obj.profile.get_role_display()
        return "Sem perfil"

    get_role.short_description = "Função"


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone", "created_at")
    list_filter = ("role", "created_at")
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "phone",
    )


@admin.register(Feeder)
class FeederAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "location",
        "status",
        "food_level",
        "owner",
        "last_maintenance",
    )
    list_filter = ("status", "last_maintenance", "created_at")
    search_fields = ("name", "location", "owner")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Informações Básicas", {"fields": ("name", "location", "owner")}),
        (
            "Status e Configuração",
            {"fields": ("status", "food_level", "capacity", "daily_consumption")},
        ),
        (
            "Manutenção e Alimentação",
            {"fields": ("last_maintenance", "next_feeding_time")},
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = (
        "feeder_name",
        "type",
        "severity",
        "resolved",
        "created_at",
        "resolved_at",
    )
    list_filter = ("type", "severity", "resolved", "created_at")
    search_fields = ("feeder__name", "message")
    fields = (
        "feeder",
        "type",
        "severity",
        "resolved",
        "created_at",
        "resolved_at",
        "message",
    )


@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ("feeder", "performed_by", "date_performed", "cost")
    list_filter = ("date_performed", "feeder")
    search_fields = ("feeder__name", "performed_by__username", "description")
    raw_id_fields = ("feeder", "performed_by")


@admin.register(FeedingLog)
class FeedingLogAdmin(admin.ModelAdmin):
    list_display = ("feeder", "amount_dispensed", "timestamp", "success")
    list_filter = ("success", "timestamp", "feeder")
    search_fields = ("feeder__name", "error_message")
    readonly_fields = ("timestamp",)
    raw_id_fields = ("feeder",)


# Customize admin site
admin.site.site_header = "AgroFeeder - Administração"
admin.site.site_title = "AgroFeeder Admin"
admin.site.index_title = "Painel de Administração"
