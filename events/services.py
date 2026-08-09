import logging
from .models import Event
from .tasks import process_event

logger = logging.getLogger('events')


def create_event(validated_data: dict) -> Event:
    event = Event.objects.create(**validated_data)
    logger.info(f"Event created: id={event.id} machine={event.machine_id}")

    process_event.delay(event.id)

    return event


def get_event_or_none(event_id: int) -> Event | None:
    return Event.objects.filter(pk=event_id).first()
