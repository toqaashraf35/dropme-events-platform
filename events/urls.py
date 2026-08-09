from django.urls import path
from .views import EventListCreateView, EventDetailView, HealthView, ReadyView, events_dashboard

urlpatterns = [
    path('events', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>', EventDetailView.as_view(), name='event-detail'),
    path('health', HealthView.as_view(), name='health'),
    path('ready', ReadyView.as_view(), name='ready'),
    path('dashboard', events_dashboard, name='events-dashboard'),

]