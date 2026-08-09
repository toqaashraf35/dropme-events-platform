import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from events.models import Event


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_event_success(api_client):
    payload = {
        "machine_id": "RVM-001",
        "material_type": "PET",
        "item_count": 5,
        "event_timestamp": timezone.now().isoformat(),
    }
    response = api_client.post("/events", payload, format="json")

    assert response.status_code == 201
    assert response.data["success"] is True
    assert response.data["data"]["machine_id"] == "RVM-001"


@pytest.mark.django_db
def test_create_event_missing_machine_id_fails(api_client):
    payload = {
        "material_type": "PET",
        "item_count": 5,
        "event_timestamp": timezone.now().isoformat(),
    }
    response = api_client.post("/events", payload, format="json")

    assert response.status_code == 400
    assert response.data["success"] is False


@pytest.mark.django_db
def test_list_events(api_client):
    Event.objects.create(
        machine_id="RVM-001",
        material_type="PET",
        item_count=5,
        event_timestamp=timezone.now(),
    )
    response = api_client.get("/events")

    assert response.status_code == 200
    assert len(response.data["data"]) == 1


@pytest.mark.django_db
def test_get_single_event_not_found(api_client):
    response = api_client.get("/events/999")
    assert response.status_code == 404


@pytest.mark.django_db
def test_health_check(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200