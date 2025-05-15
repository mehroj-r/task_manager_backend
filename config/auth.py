import base64

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

from app.models import TelegramUser


class TelegramBotAuth(BaseAuthentication):
    def authenticate(self, request):

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("BotAuth "):
            return None

        encoded_part = auth_header.split(" ", 1)[1]
        try:
            decoded = base64.b64decode(encoded_part).decode("utf-8")
            telegram_id, api_key = decoded.split(":", 1)
        except Exception:
            raise AuthenticationFailed("Invalid BotAuth format")

        if api_key != settings.BOT_API_KEY:
            raise AuthenticationFailed("Invalid API key")

        try:
            user = TelegramUser.objects.get(telegram_id=telegram_id)
        except TelegramUser.DoesNotExist:
            raise AuthenticationFailed("User not found")

        return (user, None)
