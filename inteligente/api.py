from ninja import Router, Schema
from inteligente.models import FeedingLog, Feeder
from django.utils import timezone

class FeedingLogIn(Schema):
    from_number: str
    message: str
    nivel_alerta: str

router = Router()

@router.post("/logs/feeding/")
def create_feeding_log(request, data: FeedingLogIn):
    # Buscar alimentador pelo telefone do usuário (exemplo: owner contém telefone)
    feeder = Feeder.objects.filter(owner__icontains=data.from_number).first()
    FeedingLog.objects.create(
        feeder=feeder,
        sender_phone=data.from_number,
        received_message=data.message,
        feeder_level=None,  # Pode ser ajustado se vier no JSON
        amount_dispensed=0,  # Pode ser ajustado se vier no JSON
        success=True,
        error_message=None,
        timestamp=timezone.now()
    )
    # Verificação especial para o número (541) 873-5136
    if data.from_number.replace(' ', '').replace('-', '') in ['+15418735136', '5418735136', '(541)8735136', '(541) 873-5136']:
        return {"status": "ok", "received_from": data.from_number, "special_check": True}
    return {"status": "ok"}
