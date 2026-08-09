import logging
from decimal import Decimal
from celery import shared_task
from .models import Event

logger = logging.getLogger('events')

MATERIAL_WEIGHTS = {
    'PET': Decimal('0.025'),
    'aluminum': Decimal('0.015'),
    'paper': Decimal('0.010'),
    'glass': Decimal('0.200'),
}


@shared_task
def process_event(event_id: int):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        logger.error(f"process_event: Event {event_id} not found")
        return

    weight_per_item = MATERIAL_WEIGHTS.get(event.material_type, Decimal('0.020'))
    estimated_weight = weight_per_item * event.item_count

    event.status = Event.Status.PROCESSED
    event.save(update_fields=['status'])

    logger.info(
        f"Event {event.id} processed: estimated_weight={estimated_weight}kg"
    )