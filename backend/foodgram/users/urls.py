from django.urls import path, include
from rest_framework import routers

from .views import (CustomUserViewSet, ListSubscriptions,
                    CreateDestroySubscription)

router = routers.DefaultRouter()
router.register(r'users/subscriptions', ListSubscriptions)
router.register(r'users/(?P<id>\d+)/subscribe', CreateDestroySubscription)
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
