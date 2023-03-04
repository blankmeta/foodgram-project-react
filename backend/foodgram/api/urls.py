from django.urls import path, include
from rest_framework import routers

from .views import TagViewSet, IngredientViewSet, RecipeViewSet

router = routers.DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    # path(
    #     'recipes/download_shopping_cart/',
    #     download_shopping_cart,
    #     name='download_shopping_cart'
    # ),
    # path(
    #     'users/<int:id>/subscribe/',
    #     SubscribeView.as_view(),
    #     name='subscribe'
    # ),
    # path(
    #     'users/subscriptions/',
    #     ShowSubscriptionsView.as_view(),
    #     name='subscriptions'
    # ),
    path('', include(router.urls)),
]
