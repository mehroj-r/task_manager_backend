from django.contrib import admin
from app.models import TelegramUser, Task, Remainder


@admin.register(TelegramUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'language_code', 'created_at')
    search_fields = ('id', 'username')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'due_date', 'is_completed', 'created_at')
    list_filter = ('is_completed',)
    search_fields = ('title',)

@admin.register(Remainder)
class RemainderAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'time')
    list_filter = ('user', )
    search_fields = ('task__title', )
