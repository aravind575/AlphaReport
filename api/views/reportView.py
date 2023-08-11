from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.core.exceptions import BadRequest
from django.conf import settings

import requests


class ReportInitiateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        requestData = request.data

        