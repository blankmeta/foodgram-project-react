from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Subscription

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )

        return user

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return Subscription.objects.filter(user=user, author=obj).exists()

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password', 'is_subscribed')
        model = User
