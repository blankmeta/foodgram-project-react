from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from recipes.models import ShoppingCart, Recipe, RecipeToIngredient
from recipes.models import Tag, Ingredient, Favourite
from users.models import Subscription
from .filters import RecipeFilter
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer,
                          FavouriteSerializer,
                          ShoppingCartSerializer, SubscriptionSerializer,
                          RecipePostSerializer)

User = get_user_model()


def delete_if_exists(request, id, model):
    recipe = get_object_or_404(Recipe, id=id)
    if model.objects.filter(
            user=request.user, recipe=recipe).exists():
        model.objects.filter(user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class IngredientViewSet(ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        return (super().get_serializer_class() if self.request.method == 'GET'
                else RecipePostSerializer)

    @action(['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None, *args, **kwargs):
        if request.method == 'POST':
            data = {
                'user': request.user.id,
                'recipe': pk
            }
            recipe = get_object_or_404(Recipe, id=pk)
            if not ShoppingCart.objects.filter(
                    user=request.user, recipe=recipe).exists():
                serializer = ShoppingCartSerializer(
                    data=data, context={'request': request}
                )
                if serializer.is_valid():
                    serializer.save()
                    return Response(
                        serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            return delete_if_exists(request, pk, ShoppingCart)

    @action(['post', 'delete'], detail=True)
    def favorite(self, request, pk, *args, **kwargs):
        if request.method == 'POST':
            data = {
                'user': request.user.id,
                'recipe': pk
            }
            if not Favourite.objects.filter(user=request.user,
                                            recipe__id=pk).exists():
                serializer = FavouriteSerializer(data=data,
                                                 context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data='You already have this recipe as favourite')
        elif request.method == 'DELETE':
            return delete_if_exists(request, pk, Favourite)

    @action(methods=('get',), detail=False, )
    def download_shopping_cart(self, request):
        content = "Your shopping list: \n\n"
        ingredients = RecipeToIngredient.objects.filter(
            recipe__cart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            amount=Sum('amount'))
        content += '\n'.join([
            f'{count + 1}) {ingredient["ingredient__name"]} '
            f'- {ingredient["amount"]}'
            f'{ingredient["ingredient__measurement_unit"]}'
            for count, ingredient in enumerate(ingredients)
        ])
        file = 'shopping_list'
        response = HttpResponse(content, 'Content-Type: application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file}.pdf"'
        return response


class FavouriteViewSet(ModelViewSet):
    serializer_class = FavouriteSerializer
    queryset = Favourite.objects.all()


class CreateDestroySubscribeViewSet(mixins.CreateModelMixin,
                                    mixins.DestroyModelMixin,
                                    GenericViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        id_value = self.kwargs.get('id')
        user = self.request.user
        author = User.objects.get(id=id_value)
        return Subscription.objects.get(user=user, author=author)
