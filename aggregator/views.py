import requests
from django.http import JsonResponse
from django.views import View

SEATGEEK_API_BASE_URL = "https://api.seatgeek.com/2"
CLIENT_ID = "MzkxMTQxNjV8MTcwMzUyNTI1Mi41NTY3NjI1"
CLIENT_SECRET = "a52c8f80ef7dc1990f1be5179f2099596015ec1f9c1856733b893091bed35c33"


class SeatGeekEvents(View):
    def get(self, request):
        endpoint = f"{SEATGEEK_API_BASE_URL}/events"
        params = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
        response = requests.get(endpoint, params=params)

        if response.status_code == 200:
            data = response.json()
            filtered_events = self.filter_events(data)
            return JsonResponse(filtered_events, safe=False)
        elif response.status_code == 406:
            return JsonResponse(
                {'error': '406 Not Acceptable', 'message': 'The request could not be processed by the server.'},
                status=406
            )
        else:
            return JsonResponse({'error': 'An error occurred while fetching data from SeatGeek API.'},
                                status=response.status_code)

    def filter_events(self, data):
        events = data.get('events', [])
        filtered = []
        for event in events:
            filtered_event = {
                'title': event.get('title'),
                'type': event.get('type'),
                'description': event.get('description', ''),
                'image': event['performers'][0].get('image') if event.get('performers') else '',
                'rating': event.get('score', 0),
                'organizer': {
                    'id': event['performers'][0].get('id') if event.get('performers') else '',
                    'name': event['performers'][0].get('name') if event.get('performers') else ''
                },
                'location': {
                    'lat': event['venue']['location'].get('lat') if event.get('venue') else None,
                    'lon': event['venue']['location'].get('lon') if event.get('venue') else None,
                },
                'date': event.get('datetime_utc'),
                'url': event.get('url')
            }
            filtered.append(filtered_event)
        return filtered
