from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('API-KEY')

        if api_key != settings.BOT_API_KEY:
            raise AuthenticationFailed('Invalid API Key')

        return (None, None)
