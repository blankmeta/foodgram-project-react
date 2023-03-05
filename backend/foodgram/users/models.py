from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE, )
    author = models.ForeignKey(
        User,
        related_name='subscriptions',
        on_delete=models.CASCADE, )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'author'],
                             name='unique_subscription')
        ]
