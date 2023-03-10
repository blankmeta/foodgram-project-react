from django.urls import path, include
from rest_framework import routers

from .views import CustomUserViewSet, SubscribeUserViewSet

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'users', SubscribeUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
