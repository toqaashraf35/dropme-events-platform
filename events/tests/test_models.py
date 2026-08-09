import pytest
from django.utils import timezone
from events.models import Event


@pytest.mark.django_db
def test_event_created_with_received_status_by_default():
    event = Event.objects.create(
        machine_id="RVM-001",
        material_type="PET",
        item_count=5,
        event_timestamp=timezone.now(),
    )
    assert event.status == Event.Status.RECEIVED


@pytest.mark.django_db
def test_event_string_representation():
    event = Event.objects.create(
        machine_id="RVM-001",
        material_type="PET",
        item_count=5,
        event_timestamp=timezone.now(),
    )
    assert "RVM-001" in str(event)