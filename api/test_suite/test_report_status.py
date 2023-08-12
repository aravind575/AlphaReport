from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from unittest.mock import patch

class ReportStatusViewTestCase(APITestCase):

    @patch('api.views.reportView.ReportListSerializer')
    @patch('api.views.reportView.Report')
    def test_successful_report_status(self, mock_report, mock_serializer):
        """
        Test a successful report status request to the view.
        Note: This test case has been kept simple due to time constraints of the project.
        """
        # Mock report object and serializer
        mock_report_obj = mock_report.objects.get.return_value
        mock_serializer.return_value.data = {'report_key': 'report_value'}

        # Make a request to the view
        url = reverse('report-status')
        response = self.client.get(url, {'request_id': '123'})

        # Assert response status code and data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('report_key', response.data)

    @patch('api.views.reportView.Report')
    def test_missing_request_id(self, mock_report):
        # Make a request to the view without request_id
        url = reverse('report-status')
        response = self.client.get(url)

        # Assert response status code and error handling
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Add more assertions for error handling
