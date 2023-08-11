from rest_framework import serializers
import serpy

from .models import Report


def get_report_file(request_id):
    ...


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class ReportListSerializer(serpy.Serializer):
    requestId = serpy.StrField(attr='id')
    status = serpy.StrField()
    downloadUrl = serpy.MethodField()

    def get_downloadUrl(self, obj):
        if obj.status != "COMPLETED":
            return None
        
        return get_report_file(obj.id)


