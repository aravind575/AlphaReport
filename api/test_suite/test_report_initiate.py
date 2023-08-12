from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from unittest.mock import Mock, patch

from ..views.reportView import report_generation

class ReportInitiateViewTestCase(APITestCase):

    # @patch('api.views.reportView.ReportSerializer')
    def test_successful_report_initiation(self, db):
        """
        Test a successful report initiation request to the view.
        Note: This test case has been kept simple due to time constraints of the project.
        """
        # Make a request to the view
        url = reverse('report-initiate')
        response = self.client.post(url + '?company=AAPL' + '&test=1')

        # Assert response status code and data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('request_id', response.data)
        self.assertIn('status', response.data)


    @patch('api.views.reportView.ReportSerializer')
    def test_missing_company(self, mock_serializer):
        # Make a request to the view without company parameter
        url = reverse('report-initiate')
        response = self.client.post(url)

        # Assert response status code and error handling
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Add more assertions for error handling
