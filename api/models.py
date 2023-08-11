from django.db import models

import uuid


class Report(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4())
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    