import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from unittest.mock import Mock, patch


class SearchViewTestCase(APITestCase):

    @patch('requests.get')
    def test_successful_search(self, mock_get):
        """
        Test a successful search request to the view.
        Note: This test case has been kept simple due to time constraints of the project.
        """
        mock_response = self.create_mock_response(status_code=200, json_data={
        "bestMatches": [
                {
                    "1. symbol": "TSCO.LON",
                    "2. name": "Tesco PLC",
                    "3. type": "Equity",
                    "4. region": "United Kingdom",
                    "5. marketOpen": "08:00",
                    "6. marketClose": "16:30",
                    "7. timezone": "UTC+01",
                    "8. currency": "GBX",
                    "9. matchScore": "0.7273"
                },
                {
                    "1. symbol": "TSCDF",
                    "2. name": "Tesco plc",
                    "3. type": "Equity",
                    "4. region": "United States",
                    "5. marketOpen": "09:30",
                    "6. marketClose": "16:00",
                    "7. timezone": "UTC-04",
                    "8. currency": "USD",
                    "9. matchScore": "0.7143"
                },
                {
                    "1. symbol": "TSCDY",
                    "2. name": "Tesco plc",
                    "3. type": "Equity",
                    "4. region": "United States",
                    "5. marketOpen": "09:30",
                    "6. marketClose": "16:00",
                    "7. timezone": "UTC-04",
                    "8. currency": "USD",
                    "9. matchScore": "0.7143"
                },
                {
                    "1. symbol": "TCO2.FRK",
                    "2. name": "TESCO PLC ADR/1 LS-05",
                    "3. type": "Equity",
                    "4. region": "Frankfurt",
                    "5. marketOpen": "08:00",
                    "6. marketClose": "20:00",
                    "7. timezone": "UTC+02",
                    "8. currency": "EUR",
                    "9. matchScore": "0.5455"
                },
                {
                    "1. symbol": "TCO0.FRK",
                    "2. name": "TESCO PLC LS-0633333",
                    "3. type": "Equity",
                    "4. region": "Frankfurt",
                    "5. marketOpen": "08:00",
                    "6. marketClose": "20:00",
                    "7. timezone": "UTC+02",
                    "8. currency": "EUR",
                    "9. matchScore": "0.5455"
                }
            ]
        })
        mock_get.return_value = mock_response

        url = reverse('search')
        response = self.client.get(url, {'q': 'apple'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['bestMatches']), 1)
        

    @patch('requests.get')
    def test_failed_search(self, mock_get):
        mock_response = self.create_mock_response(status_code=500)
        mock_get.return_value = mock_response

        url = reverse('search')
        response = self.client.get(url, {'q': 'apple'})

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Add more assertions for error handling

    def create_mock_response(self, status_code, json_data=None):
        mock_response = Mock()
        mock_response.status_code = status_code
        if json_data:
            mock_response.json.return_value = json_data
        return mock_response
