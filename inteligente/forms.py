from django import forms
from django.db import models
from .models import (
    Agricultor,
    Animal,
    User,
    Alimentador,
    Alimento,
    Visitante,
    Relatorio,
    UserProfile,
    Feeder,
    Alert,
    MaintenanceLog,
    FeedingLog,
)


class agricultorForm(forms.ModelForm):
    class Meta:
        model = Agricultor
        fields = "__all__"


class animalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = "__all__"


class alimentadorForm(forms.ModelForm):
    class Meta:
        model = Alimentador
        fields = "__all__"


class alimentoForm(forms.ModelForm):
    class Meta:
        model = Alimento
        fields = "__all__"


class visitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = "__all__"


class feederForm(forms.ModelForm):
    class Meta:
        model = Feeder
        fields = [
            "name",
            "location",
            "owner",
            "status",
            "food_level",
            "capacity",
            "daily_consumption",
            "last_maintenance",
            "next_maintenance",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Digite o nome do alimentador"}
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Digite a localização do alimentador"}
            ),
            "owner": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Digite o nome do proprietário"}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
            "food_level": forms.NumberInput(
                attrs={"class": "form-control", "min": 0, "max": 100}
            ),
            "capacity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "daily_consumption": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "last_maintenance": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "next_maintenance": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }


class FarmerFeederForm(forms.ModelForm):
    """Formulário simplificado para agricultores"""

    class Meta:
        model = Feeder
        fields = [
            "name",
            "location",
            "status",
            "food_level",
            "capacity",
            "daily_consumption",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Digite o nome do alimentador"}
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Digite a localização do alimentador"}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
            "food_level": forms.NumberInput(
                attrs={"class": "form-control", "min": 0, "max": 100}
            ),
            "capacity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "daily_consumption": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
        }
        labels = {
            "name": "Nome do Alimentador",
            "location": "Localização",
            "status": "Status",
            "food_level": "Nível de Ração (%)",
            "capacity": "Capacidade (kg)",
            "daily_consumption": "Consumo Diário (kg)",
        }


class alertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ["feeder", "type", "message", "severity"]
        widgets = {
            "feeder": forms.Select(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-control"}),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Digite a descrição do alerta",
                }
            ),
            "severity": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "feeder": "Alimentador",
            "type": "Tipo do Alerta",
            "message": "Mensagem",
            "severity": "Severidade",
        }


class FarmerAlertForm(forms.ModelForm):
    """Formulário de alertas para agricultores"""

    class Meta:
        model = Alert
        fields = ["feeder", "type", "message", "severity"]
        widgets = {
            "feeder": forms.Select(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-control"}),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Digite a descrição do alerta",
                }
            ),
            "severity": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "feeder": "Alimentador",
            "type": "Tipo do Alerta",
            "message": "Mensagem",
            "severity": "Severidade",
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            user_full_name = user.get_full_name() or user.username
            self.fields["feeder"].queryset = Feeder.objects.filter(owner=user_full_name)

        self.fields["feeder"].empty_label = "Selecione um alimentador"


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirme a Senha"
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]
        labels = {
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "email": "E-mail",
            "username": "Nome de usuário",
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este e-mail já está cadastrado no sistema. Por favor, use outro e-mail."
            )
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    {
                        "confirm_password": "As senhas não coincidem. Digite a mesma senha nos dois campos."
                    }
                )
        elif password and not confirm_password:
            raise forms.ValidationError(
                {"confirm_password": "Por favor, confirme a senha."}
            )
        elif not password and confirm_password:
            raise forms.ValidationError({"password": "Por favor, digite a senha."})

        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["role", "phone", "address"]
        labels = {
            "role": "Função",
            "phone": "Telefone",
            "address": "Endereço",
        }
        widgets = {
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Digite o número de telefone do usuário"}
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Digite o endereço do usuário",
                }
            ),
        }


class FarmerProfileForm(forms.ModelForm):
    """Formulário para agricultores editarem seu próprio perfil"""

    class Meta:
        model = UserProfile
        fields = ["phone", "address", "custom_executive_summary"]
        widgets = {
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Digite seu número de telefone"}
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Digite seu endereço completo",
                }
            ),
            "custom_executive_summary": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Digite seu resumo executivo personalizado",
                }
            ),
        }
        labels = {
            "phone": "Telefone",
            "address": "Endereço",
            "custom_executive_summary": "Resumo Executivo Personalizado",
        }
        help_texts = {
            "custom_executive_summary": "Este texto será exibido na seção de resumo executivo dos seus relatórios. Você pode incluir informações sobre sua operação, objetivos, observações, etc.",
        }
