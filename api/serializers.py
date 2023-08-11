from rest_framework import serializers
import serpy

from .models import Report, BalanceSheet

import logging

import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from boto3.session import Config

from django.conf import settings


session = boto3.Session()
s3 = session.client("s3",region_name='eu-central-1',config=Config(signature_version="s3v4"))


def getPresignedUrl(report_id, expiration=3600, bucket=None):
    try:
        fileKey = f"{report_id}.pdf"
        s3.head_object(Bucket=settings.BUCKET_NAME, Key=fileKey)
        response = s3.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket if bucket is not None else settings.BUCKET_NAME,
                                                            'Key': fileKey},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return False

    return response


def storeFileInBucket(file, fileKey, bucket=None):
    try:
        s3.upload_fileobj(file, 
                        Bucket= bucket if bucket is not None else settings.BUCKET_NAME)
    except ClientError as e:
        logging.error(e)
        return False
    
    return "DONE"


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
        
        return getPresignedUrl(obj.id)
    

class BalanceSheetSerializer(serializers.Serializer):
    class Meta:
        model = BalanceSheet
        fields = '__all__'
    

class BalanceSheetListSerializer(serpy.Serializer):
    id = serpy.StrField()
    data = serpy.Field()
    report_id = serpy.StrField()


