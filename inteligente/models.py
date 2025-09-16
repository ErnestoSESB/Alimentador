from django.db import models

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
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="perfil_agricultor")
    farm_name = models.CharField(max_length=60, blank=True)
    city = models.CharField(max_length=60, blank=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.name
    

class Animal(models.Model):
    SIZES = [
        ("small", "Pequeno"),
        ("medium", "Medio"),
        ("large", "Grande")
    ]
    type = models.CharField(max_length=30)
    size = models.CharField(max_length=20, choices=SIZES)
    feed_value = models.IntegerField()
    farmer = models.ForeignKey(Agricultor, on_delete=models.CASCADE, related_name="animals")
    foods = models.ManyToManyField('Alimento', related_name='animals')

    def __str__(self):
        return self.type
    
class Alimentador(models.Model):
    owner = models.ForeignKey(Agricultor, on_delete=models.CASCADE, related_name='feeders')
    model = models.CharField(max_length=50)
    capacity = models.DecimalField(max_digits=6, decimal_places=2, help_text="Maximum capacity in kg")
    feed_level = models.DecimalField(max_digits=6, decimal_places=2, help_text="Current feed level in kg")
    last_maintenance_date = models.DateField()

    def __str__(self):
        return f"{self.model} ({self.owner.user.name})"

class Alimento(models.Model):
    feeder = models.ForeignKey(Alimentador, on_delete=models.CASCADE, related_name="feeds")
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
    feeder = models.ForeignKey(Alimentador, on_delete=models.CASCADE, related_name='reports')
    monthly_consumption = models.DecimalField(max_digits=8, decimal_places=2, help_text="Feed consumption in the month (kg)")
    efficiency = models.DecimalField(max_digits=5, decimal_places=2, help_text="Efficiency in %")
    maintenances = models.TextField(blank=True, help_text="Description of maintenances")
    total_consumption = models.DecimalField(max_digits=8, decimal_places=2, help_text="Total feed consumption (kg)")
    machine_status = models.CharField(max_length=40, help_text="Current status of the feeder")
    report_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Report {self.id} - {self.feeder.model}"
