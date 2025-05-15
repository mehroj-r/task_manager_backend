from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.views import UserViewSet, TaskViewSet, RemainderViewSet

urlpatterns = [

]

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('tasks', TaskViewSet, basename='tasks')
router.register('remainders', RemainderViewSet, basename='remainders')
urlpatterns += router.urls