from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.core.exceptions import BadRequest
from django.conf import settings

import requests


class SearchView(APIView):
    # Allow unauthenticated access for company search
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Extract search query from query parameters
        query = request.query_params.get('q', None)

        if query is None:
            raise BadRequest('Query parameter "q" is missing.')
        
        # Get API configurations from settings
        base_url = settings.ALPHA_SEARCH_URL
        function = settings.ALPHA_SEARCH_FUNCTION
        apikey = settings.ALPHA_API_KEY

        # Set parameters for the search API request
        params = {
            'function': function,
            'keywords': query,
            'apikey': apikey
        }

        # Make a request to the search API
        response = requests.get(base_url, params=params)
        
        # format and return response data if response is successful
        if response.status_code == 200:
            result_key = 'bestMatches'
            formatted_data = self.format_response_data(response.json().get(result_key))
            return Response({result_key: formatted_data}, status=status.HTTP_200_OK)
        
        # Return an error response if the API request fails
        return Response({'error': 'An error occurred while fetching data.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def format_response_data(self, list_of_dicts):
        """
        Formats the response data received from the AlphaVantage API.

        :param list_of_dicts: List of dictionaries containing raw API response data.
        :return: Formatted list of dictionaries with relevant information.
        """
        formatted_data = []
        for entry in list_of_dicts:
            # explicit creation for better performance, as opposed to dynamically altering the keys
            formatted_entry = {
                'symbol': entry.get('1. symbol'),
                'name': entry.get('2. name'),
                'type': entry.get('3. type'),
                'region': entry.get('4. region'),
                'marketOpen': entry.get('5. marketOpen'),
                'marketClose': entry.get('6. marketClose'),
                'timezone': entry.get('7. timezone'),
                'currency': entry.get('8. currency'),
                'matchScore': entry.get('9. matchScore'),
            }
            formatted_data.append(formatted_entry)
        return formatted_data
