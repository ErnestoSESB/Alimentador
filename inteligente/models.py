from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Usuario(models.Model):
    CATEGORIES = [
        ("ADMIN", "Administrador"),
        ("AGRIC", "Agricultor"),
        ("VISIT", "Visitante"),
    ]

    name = models.CharField(max_length=60)
    category = models.CharField(max_length=6, choices=CATEGORIES)
    phone = models.CharField(max_length=20, blank=True)
    active = models.BooleanField(default=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Agricultor(models.Model):
    user = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_agricultor"
    )
    farm_name = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=60, blank=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.name


class Animal(models.Model):
    SIZES = [("small", "Pequeno"), ("medium", "Medio"), ("large", "Grande")]
    type = models.CharField(max_length=30)
    size = models.CharField(max_length=20, choices=SIZES)
    feed_value = models.IntegerField()
    farmer = models.ForeignKey(
        Agricultor, on_delete=models.CASCADE, related_name="animals"
    )
    foods = models.ManyToManyField("Alimento", related_name="animals")

    def __str__(self):
        return self.type


class Alimentador(models.Model):
    owner = models.ForeignKey(
        Agricultor, on_delete=models.CASCADE, related_name="feeders"
    )
    model = models.CharField(max_length=50)
    capacity = models.DecimalField(
        max_digits=6, decimal_places=2, help_text="Maximum capacity in kg"
    )
    feed_level = models.DecimalField(
        max_digits=6, decimal_places=2, help_text="Current feed level in kg"
    )
    last_maintenance_date = models.DateField()

    def __str__(self):
        return f"{self.model} ({self.owner.user.name})"


class Alimento(models.Model):
    feeder = models.ForeignKey(
        Alimentador, on_delete=models.CASCADE, related_name="feeds"
    )
    name = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Visitante(models.Model):
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f"Visitor {self.id}"


class Relatorio(models.Model):
    feeder = models.ForeignKey(
        Alimentador, on_delete=models.CASCADE, related_name="reports"
    )
    monthly_consumption = models.DecimalField(
        max_digits=8, decimal_places=2, help_text="Feed consumption in the month (kg)"
    )
    efficiency = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Efficiency in %"
    )
    maintenances = models.TextField(blank=True, help_text="Description of maintenances")
    total_consumption = models.DecimalField(
        max_digits=8, decimal_places=2, help_text="Total feed consumption (kg)"
    )
    machine_status = models.CharField(
        max_length=40, help_text="Current status of the feeder"
    )
    report_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Report {self.id} - {self.feeder.model}"


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Administrador"),
        ("farmer", "Agricultor"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="farmer")
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_by_admin = models.BooleanField(
        default=False, verbose_name="Criado por Administrador"
    )
    custom_executive_summary = models.TextField(
        blank=True, null=True, verbose_name="Resumo Executivo Personalizado"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_role_display()}"

    @property
    def is_admin(self):
        return self.user.is_superuser or self.role == "admin"


class Feeder(models.Model):
    """Animal feeder model"""

    STATUS_CHOICES = [
        ("active", "Ativo"),
        ("inactive", "Inativo"),
        ("maintenance", "Manutenção"),
        ("error", "Erro"),
    ]

    name = models.CharField(max_length=100, verbose_name="Nome")
    location = models.CharField(max_length=200, verbose_name="Localização")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="inactive", verbose_name="Status"
    )
    food_level = models.IntegerField(default=0, verbose_name="Nível de Ração (%)")
    last_maintenance = models.DateField(
        default=timezone.now, verbose_name="Última Manutenção"
    )
    owner = models.CharField(max_length=100, verbose_name="Proprietário")
    capacity = models.IntegerField(default=500, verbose_name="Capacidade (kg)")
    daily_consumption = models.IntegerField(
        default=25, verbose_name="Consumo Diário (kg)"
    )
    next_feeding_time = models.DateTimeField(
        default=timezone.now, verbose_name="Próxima Alimentação"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    next_maintenance = models.DateField(
        null=True, blank=True, verbose_name="Próxima Manutenção"
    )

    class Meta:
        verbose_name = "Alimentador"
        verbose_name_plural = "Alimentadores"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def is_low_food(self):
        """Check if food level is low"""
        return self.food_level < 20

    @property
    def needs_maintenance(self):
        """Check if maintenance is needed"""
        from datetime import date, timedelta

        return (date.today() - self.last_maintenance).days > 30


class Alert(models.Model):
    TYPE_CHOICES = [
        ("low_food", "Nível Baixo de Ração"),
        ("maintenance", "Manutenção Necessária"),
        ("error", "Erro no Sistema"),
        ("offline", "Equipamento Offline"),
    ]

    SEVERITY_CHOICES = [
        ("low", "Baixo"),
        ("medium", "Médio"),
        ("high", "Alto"),
    ]

    # alert_id = models.UUIDField(default=uuid.uuid4,unique=True, editable=False, null=False, blank=False)
    feeder = models.ForeignKey(
        "Feeder", on_delete=models.CASCADE, related_name="alerts"
    )
    feeder_name = models.CharField(
        max_length=100, verbose_name="Nome do Alimentador"
    )  # Campo obrigatório
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField(verbose_name="Mensagem")
    severity = models.CharField(
        max_length=10, choices=SEVERITY_CHOICES, default="medium"
    )
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(verbose_name="Criado em")
    resolved_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Resolvido em"
    )

    def save(self, *args, **kwargs):
        if self.feeder and not self.feeder_name:
            self.feeder_name = self.feeder.name
        super().save(*args, **kwargs)

    def feeder_name(self):
        return self.feeder.name

    feeder_name.short_description = "Nome do Alimentador"

    def __str__(self):
        return f"{self.feeder.name} - {self.get_type_display()}"


class MaintenanceLog(models.Model):
    """Maintenance log model"""

    feeder = models.ForeignKey(
        Feeder, on_delete=models.CASCADE, related_name="maintenance_logs"
    )
    performed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Descrição")
    date_performed = models.DateTimeField(
        default=timezone.now, verbose_name="Data da Manutenção"
    )
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Custo"
    )

    class Meta:
        verbose_name = "Log de Manutenção"
        verbose_name_plural = "Logs de Manutenção"
        ordering = ["-date_performed"]

    def __str__(self):
        return f"{self.feeder.name} - {self.date_performed.strftime('%d/%m/%Y')}"


class FeedingLog(models.Model):
    """Feeding log model"""

    feeder = models.ForeignKey(
        Feeder, on_delete=models.CASCADE, related_name="feeding_logs"
    )
    amount_dispensed = models.IntegerField(verbose_name="Quantidade Dispensada (kg)")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Data/Hora")
    success = models.BooleanField(default=True, verbose_name="Sucesso")
    error_message = models.TextField(
        blank=True, null=True, verbose_name="Mensagem de Erro"
    )

    class Meta:
        verbose_name = "Log de Alimentação"
        verbose_name_plural = "Logs de Alimentação"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.feeder.name} - {self.timestamp.strftime('%d/%m/%Y %H:%M')}"


class MonthlyConsumption(models.Model):
    """Stores simulated monthly consumption (kg) for each feeder."""
    feeder = models.ForeignKey(Feeder, on_delete=models.CASCADE, related_name='monthly_consumptions')
    year = models.IntegerField()
    month = models.IntegerField()
    kg_consumed = models.FloatField(default=0.0)

    class Meta:
        unique_together = (('feeder', 'year', 'month'),)
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.feeder.name} - {self.month}/{self.year}: {self.kg_consumed}kg"
