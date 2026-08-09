from django.db import models


class Event(models.Model):
    class Status(models.TextChoices):
        RECEIVED = 'received', 'Received'
        PROCESSED = 'processed', 'Processed'

    class MaterialType(models.TextChoices):
        PET = 'PET', 'PET Plastic'
        ALUMINUM = 'aluminum', 'Aluminum'
        PAPER = 'paper', 'Paper'
        GLASS = 'glass', 'Glass'

    machine_id = models.CharField(max_length=50)
    material_type = models.CharField(max_length=20, choices=MaterialType.choices)
    item_count = models.PositiveIntegerField()
    event_timestamp = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.RECEIVED,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.machine_id} - {self.material_type} ({self.status})"
