from rest_framework import serializers

from app.models import TelegramUser, Task, Remainder


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TelegramUser
        fields = ('username', 'first_name', 'last_name', 'telegram_id', 'language_code', 'created_at')


class TaskSerializer(serializers.ModelSerializer):

    due_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", required=False)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'user', 'description', 'due_date', 'created_at')

class RemainderSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    time = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")

    class Meta:
        model = Remainder
        fields = ('id', 'task', 'user', 'time', 'created_at')