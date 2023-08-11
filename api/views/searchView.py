from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.core.exceptions import BadRequest
from django.conf import settings

import requests


class SearchView(APIView):
    permission_classes = [AllowAny]

    
    def get(self, request):
        query = request.query_params.get('q', None)
        print(query)

        if query is None:
            raise BadRequest('Query parameter is missing.')
        
        base_url = settings.ALPHA_SEARCH_PATH
        function = settings.ALPHA_SEARCH_FUNCTION
        keywords = query
        apikey = settings.ALPHA_API_KEY

        params = {
            'function': function,
            'keywords': keywords,
            'apikey': apikey
        }

        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            result_key = 'bestMatches'
            formatted_data = self.format_response_data(response.json().get(result_key))
            return Response({result_key: formatted_data}, status=status.HTTP_200_OK)
        
        return Response({'error': 'An error occurred while fetching data.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def format_response_data(self, list_of_dicts):
        formatted_data = []
        for entry in list_of_dicts:
            # explicit creation for better performance
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
    