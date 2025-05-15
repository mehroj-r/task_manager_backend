from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from app.models import TelegramUser, Task, Remainder
from .serializers import UserSerializer, TaskSerializer, RemainderSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Telegram users.
    """
    queryset = TelegramUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class TaskViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Tasks, filtered by user.
    """
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user is not None:
            return Task.objects.filter(user=user)
        return Task.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RemainderViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Reminders, filtered by user.
    """
    serializer_class = RemainderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user is not None:
            return Remainder.objects.filter(user=user)
        return Remainder.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)