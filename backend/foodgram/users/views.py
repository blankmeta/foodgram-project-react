from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.pagination import PageLimitPagination
from api.serializers import SubscriptionSerializer
from .models import Subscription
from .serializers import UserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageLimitPagination


class ListSubscriptions(mixins.ListModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageLimitPagination

    def list(self, request, *args, **kwargs):
        pages = self.paginate_queryset(
            User.objects.filter(subscriptions__user=self.request.user)
        )
        serializer = SubscriptionSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)


class CreateDestroySubscription(mixins.CreateModelMixin,
                                mixins.DestroyModelMixin,
                                GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageLimitPagination

    def create(self, request, *args, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        serializer = SubscriptionSerializer(author,
                                            data=request.data,
                                            context={"request": request})
        serializer.is_valid(raise_exception=True)
        Subscription.objects.create(user=user, author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        subscription = get_object_or_404(Subscription,
                                         user=user,
                                         author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
