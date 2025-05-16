from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils import verify_telegram_signature
from app.models import TelegramUser


class AuthAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        # Extract body
        telegram_id = request.data.get('id')
        signed_hash = request.data.get('hash')

        if not telegram_id or not str(telegram_id).isdigit() or not signed_hash:
            return Response({'detail':'Missing id or hash.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the signature of hash
        data = verify_telegram_signature(signed_hash, settings.BOT_API_SECRET)

        # Check conditions that make the request invalid
        if data == -1:
            return Response({'detail': 'Expired signature.'}, status=status.HTTP_400_BAD_REQUEST)

        if data == -2:
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        if telegram_id != data['id']:
            return Response({'detail': 'Tampered token.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new uer if already isn't created
        try:
            user = TelegramUser.objects.get(id=telegram_id)
        except TelegramUser.DoesNotExist:
            user = TelegramUser.objects.create_user(**data)

        # Manually generate token
        refresh = RefreshToken.for_user(user)

        return Response({
            'token': str(refresh.access_token),
            'refresh': str(refresh),
        })
