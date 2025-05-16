from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from app.models import TelegramUser


class AuthAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        telegram_id = request.data.get('id')

        if not telegram_id or not str(telegram_id).isdigit():
            return Response({'detail':'Invalid or missing ID'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = TelegramUser.objects.get(id=int(telegram_id))
        except TelegramUser.DoesNotExist:
            return Response({'detail':'Authentication failed'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)

        return Response({
            'token':str(refresh.access_token),
            'refresh':str(refresh),
        })
