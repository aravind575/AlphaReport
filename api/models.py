from django.db import models
from django.db.models import CASCADE, DO_NOTHING, JSONField
import uuid


class Report(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4())
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')


class BalanceSheet(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4())
    data = JSONField(null=False)
    report = models.ForeignKey(Report, on_delete=DO_NOTHING)
    