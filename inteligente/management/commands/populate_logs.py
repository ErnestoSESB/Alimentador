from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inteligente.models import Feeder, ActivityLog, MaintenanceLog, FeedingLog
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Popula o banco de dados com logs de exemplo'

    def handle(self, *args, **kwargs):
        self.stdout.write('Criando logs de exemplo...')

        users = list(User.objects.all())
        feeders = list(Feeder.objects.all())

        if not users:
            self.stdout.write(self.style.ERROR('Nenhum usuário encontrado. Crie usuários primeiro.'))
            return

        if not feeders:
            self.stdout.write(self.style.ERROR('Nenhum alimentador encontrado. Crie alimentadores primeiro.'))
            return


        actions = ['create', 'update', 'login', 'logout', 'feeding', 'maintenance', 'alert']
        descriptions = {
            'create': 'Novo alimentador criado no sistema',
            'update': 'Configurações do alimentador atualizadas',
            'login': 'Login realizado no sistema',
            'logout': 'Logout do sistema',
            'feeding': 'Alimentação automática executada',
            'maintenance': 'Manutenção preventiva realizada',
            'alert': 'Novo alerta gerado pelo sistema',
        }

        for i in range(30):
            action = random.choice(actions)
            user = random.choice(users)
            feeder = random.choice(feeders) if action not in ['login', 'logout'] else None
            
            ActivityLog.objects.create(
                user=user,
                feeder=feeder,
                action=action,
                description=descriptions[action],
                timestamp=timezone.now() - timedelta(days=random.randint(0, 30)),
                ip_address=f'192.168.1.{random.randint(1, 254)}'
            )

        self.stdout.write(self.style.SUCCESS('30 logs de atividades criados!'))

        maintenance_descriptions = [
            'Limpeza completa do sistema de alimentação',
            'Substituição de componentes desgastados',
            'Calibração dos sensores de nível',
            'Verificação do sistema elétrico',
            'Atualização do firmware',
        ]

        for i in range(15):
            MaintenanceLog.objects.create(
                feeder=random.choice(feeders),
                performed_by=random.choice(users),
                description=random.choice(maintenance_descriptions),
                date_performed=timezone.now() - timedelta(days=random.randint(0, 60)),
                cost=round(random.uniform(50, 500), 2)
            )

        self.stdout.write(self.style.SUCCESS('15 logs de manutenção criados!'))

        for i in range(50):
            success = random.random() > 0.1 
            FeedingLog.objects.create(
                feeder=random.choice(feeders),
                amount_dispensed=random.randint(5, 50),
                timestamp=timezone.now() - timedelta(hours=random.randint(0, 720)),
                success=success,
            )

        self.stdout.write(self.style.SUCCESS('50 logs de alimentação criados!'))
        self.stdout.write(self.style.SUCCESS('Todos os logs foram criados com sucesso!'))
