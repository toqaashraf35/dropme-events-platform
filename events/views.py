from rest_framework.views import APIView
from django.db import connection
from django.conf import settings
import redis
from django.shortcuts import render

from .models import Event
from .serializers import EventSerializer
from .services import create_event, get_event_or_none
from .responses import success_response, error_response


class EventListCreateView(APIView):

    def get(self, request):
        events = Event.objects.all().order_by('-created_at')
        serializer = EventSerializer(events, many=True)
        return success_response(data=serializer.data, message="Events retrieved")

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Validation failed",
                errors=serializer.errors,
                status_code=400,
            )

        event = create_event(serializer.validated_data)
        result = EventSerializer(event)
        return success_response(
            data=result.data,
            message="Event created",
            status_code=201,
        )


class EventDetailView(APIView):

    def get(self, request, pk):
        event = get_event_or_none(pk)
        if event is None:
            return error_response(
                message="Event not found",
                errors=None,
                status_code=404,
            )

        serializer = EventSerializer(event)
        return success_response(data=serializer.data, message="Event retrieved")


class HealthView(APIView):
    def get(self, request):
        return success_response(data={"status": "up"}, message="Service is healthy")


class ReadyView(APIView):
    def get(self, request):
        checks = {}
        healthy = True

        try:
            connection.ensure_connection()
            checks['database'] = 'ok'
        except Exception as e:
            checks['database'] = f'error: {e}'
            healthy = False

        try:
            r = redis.Redis.from_url(settings.REDIS_URL)
            r.ping()
            checks['redis'] = 'ok'
        except Exception as e:
            checks['redis'] = f'error: {e}'
            healthy = False

        if healthy:
            return success_response(data=checks, message="Service is ready")
        return error_response(message="Service not ready", errors=checks, status_code=503)


def events_dashboard(request):
    events = Event.objects.all().order_by('-created_at')[:100]
    return render(request, 'events/dashboard.html', {'events': events})