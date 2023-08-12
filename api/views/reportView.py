from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.core.exceptions import BadRequest
from django.conf import settings

import requests
import threading
import logging

from ..models import Report
from ..serializers import ReportSerializer, ReportListSerializer, BalanceSheetSerializer

from ..scripts.report import upload_pdf_to_s3


# init logger
logger = logging.getLogger(__name__)



class ReportStatusView(APIView):
    # Allow unauthenticated access for checking report status
    permission_classes = [AllowAny]

    def get(self, request):
        # Extract request ID from query parameters
        request_id = request.query_params.get('request_id', None)

        if request_id is None:
            logger.error('Request ID is missing.')
            raise BadRequest('Request ID is missing.')
        
        try:
            # Retrieve report object from the database
            report = Report.objects.get(id=request_id)
            reportData = ReportListSerializer(report).data
        except Report.DoesNotExist:
            logger.error(f'Report with ID {request_id} does not exist.')
            raise BadRequest(f'Report with ID {request_id} does not exist.')
        
        return Response(reportData, status=status.HTTP_200_OK)

class ReportInitiateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Extract company symbol from query parameters
        company = request.query_params.get('company', None)
        test = request.query_params.get('test', None)

        if company is None:
            logger.error('Company is missing.')
            raise BadRequest('Company is missing.')
        
        
        # Create an report object with a unique request_id
        serializer = ReportSerializer(data={})
        serializer.is_valid(raise_exception=True)
        report = serializer.save()

        # Spawn a thread to execute the report generation asynchronously
        if test is not None:
            thread_balance_sheet = threading.Thread(target=report_generation, args=(report.id, company))
            thread_balance_sheet.start()

        return Response({
            "request_id": report.id,
            "status": report.status
        }, status=status.HTTP_201_CREATED)

def report_generation(report_id, company):
    # Get API configurations from settings
    apikey = settings.ALPHA_API_KEY
    base_url = settings.ALPHA_URL
    bs_function = settings.ALPHA_BALANCE_SHEET_FUNCTION
    news_function = settings.ALPHA_NEWS_FUNCTION

    try:
        # Set parameters for balance sheet API
        bs_params = {
            'function': bs_function,
            'symbol': company,
            'apikey': apikey
        }

        # Make a request to the balance sheet API
        bs_response = requests.get(base_url, params=bs_params)
        balanceSheet = bs_response.json()

        # Set parameters for news API
        news_params = {
            'function': news_function,
            'tickers': company,
            'apikey': apikey
        }

        # Make a request to the news API
        news_response = requests.get(base_url, params=news_params)
        news = news_response.json()

        # Save balance sheet data to the database
        serializer = BalanceSheetSerializer(data={
            "data": balanceSheet,
            "report": report_id
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Upload the generated PDF (including balance sheet data and news data) report to S3
        upload_pdf_to_s3(balanceSheet, news, report_id)
        logger.info(f"Report generation completed for request_id: {report_id}")

    except Exception as e:
        logger.error(f"Error generating report for request_id {report_id}: {e}")

    return
