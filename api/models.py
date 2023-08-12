from django.db import models
from django.db.models import DO_NOTHING, JSONField
import uuid

class Report(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    # Unique identifier for the report
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    
    # Status of the report, defaults to 'PENDING'
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Report {self.id} - {self.status}"


class BalanceSheet(models.Model):
    # Unique identifier for the balance sheet
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4)
    
    # JSON field to store balance sheet data
    data = JSONField(null=False)
    
    # ForeignKey relationship to connect the balance sheet to a report
    report = models.ForeignKey(Report, on_delete=DO_NOTHING)

    def __str__(self):
        return f"BalanceSheet {self.id} - Report {self.report.id}"
