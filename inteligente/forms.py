from django import forms
from .models import Agricultor, Animal, User, Alimentador, Alimento, Visitante, Relatorio, UserProfile, Feeder, Alert, MaintenanceLog, FeedingLog

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

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirme a Senha")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }

    #Aqui faz a validação para não repetir o email do usuario e quebrar essa bosta
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado no sistema. Por favor, use outro e-mail.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError({
                    'confirm_password': 'As senhas não coincidem. Digite a mesma senha nos dois campos.'
                })
        elif password and not confirm_password:
            raise forms.ValidationError({
                'confirm_password': 'Por favor, confirme a senha.'
            })
        elif not password and confirm_password:
            raise forms.ValidationError({
                'password': 'Por favor, digite a senha.'
            })
            
        return cleaned_data
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role', 'phone', 'address']