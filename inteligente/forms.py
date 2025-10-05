from django import forms
from .models import Agricultor, Animal, Usuario, Alimentador, Alimento, Visitante, Relatorio, UserProfile, Feeder, Alert, MaintenanceLog, FeedingLog

class agricultorForm(forms.ModelForm):
    class Meta:
        model = Agricultor
        fields = '__all__'
        
class animalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = '__all__'

class alimentadorForm(forms.ModelForm):
    class Meta:
        model = Alimentador
        fields = '__all__'

class alimentoForm(forms.ModelForm):
    class Meta:
        model = Alimento
        fields = '__all__'

class visitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = '__all__'

class feederForm(forms.ModelForm):
    class Meta:
        model = Feeder
        fields = '__all__'

class alertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = '__all__'