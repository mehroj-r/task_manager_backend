from django.core.management.base import BaseCommand
from rest_framework_simplejwt.tokens import RefreshToken

from app.models import TelegramUser


class Command(BaseCommand):
    help = 'This command generates a valid token and hash'

    def handle(self, *args, **options):
        telegram_id = 1316712488
        new_token = RefreshToken.for_user(TelegramUser.objects.get(pk=telegram_id))
        print(new_token.access_token)