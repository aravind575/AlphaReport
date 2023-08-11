from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.core.exceptions import BadRequest
from django.conf import settings

import requests
import threading

from ..models import Report
from ..serializers import ReportSerializer, ReportListSerializer, BalanceSheetSerializer

from ..scripts.report import upload_pdf_to_s3


class ReportStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_id = request.query_params.get('request_id', None)

        if request_id is None:
            raise BadRequest('Request ID is missing.')
        
        report = Report.objects.get(id=request_id)
        reportData = ReportListSerializer(report).data

        return Response(reportData, status=status.HTTP_200_OK)


class ReportInitiateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        company = request.query_params.get('company', None)

        if company is None:
            raise BadRequest('Company is missing.')
        
        serializer = ReportSerializer(data={})
        serializer.is_valid(raise_exception=True)
        report = serializer.save()

        # Spawn a thread to execute asynchronously
        thread_balance_sheet = threading.Thread(target=report_generation, args=(report.id, company))
        thread_balance_sheet.start()

        return Response({
            "request_id": report.id,
            "status": report.status
        }, status=status.HTTP_201_CREATED)
    

def report_generation(report_id, company):
    apikey = settings.ALPHA_API_KEY
    bs_base_url = settings.ALPHA_BALANCE_SHEET_URL
    bs_function = settings.ALPHA_BALANCE_SHEET_FUNCTION
    news_base_url = settings.ALPHA_NEWS_URL
    news_function = settings.ALPHA_NEWS_FUNCTION

    bs_params = {
        'function': bs_function,
        'symbol': company,
        'apikey': apikey
    }

    bs_response = requests.get(bs_base_url, params=bs_params)
    balanceSheet = bs_response.json()

    news_params = {
        'function': news_function,
        'symbol': company,
        'apikey': apikey
    }

    news_response = requests.get(news_base_url, params=news_params)
    news = news_response.json()

    serializer = BalanceSheetSerializer(data={
        "data": balanceSheet,
        "report": report_id
    })
    serializer.is_valid(raise_exception=True)
    serializer.save()

    upload_pdf_to_s3(balanceSheet, news, report_id)

    return




