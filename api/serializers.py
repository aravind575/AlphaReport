from rest_framework import serializers

import serpy

from .models import Report, BalanceSheet
from .scripts.s3 import getPresignedUrl


# Serializer for (creation of) the Report model
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


# Serializer for the Report model with additional field (s3-presigned-url) for list view
# Using serpy as it's "ridiculously fast"
class ReportListSerializer(serpy.Serializer):
    requestId = serpy.StrField(attr='id')
    status = serpy.StrField()
    downloadUrl = serpy.MethodField()

    # Dynamically calculate and provide download URL (only) for completed reports
    def get_downloadUrl(self, obj):
        if obj.status != "COMPLETED":
            return None
        
        fileKey = f"{obj.id}.pdf"
        return getPresignedUrl(fileKey)


# Serializer for (creation of) the BalanceSheet model
class BalanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceSheet
        fields = '__all__'


# Serializer for the BalanceSheet model with additional fields for list view
class BalanceSheetListSerializer(serpy.Serializer):
    id = serpy.StrField()
    data = serpy.Field()
    report_id = serpy.StrField()
