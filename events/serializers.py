from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'machine_id',
            'material_type',
            'item_count',
            'event_timestamp',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'status', 'created_at']

    def validate_item_count(self, value):
        if value <= 0:
            raise serializers.ValidationError("item_count must be greater than zero.")
        return value

    def validate_machine_id(self, value):
        if not value.strip():
            raise serializers.ValidationError("machine_id cannot be empty.")
        return value