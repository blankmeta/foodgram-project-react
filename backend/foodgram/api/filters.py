from django_filters import rest_framework

from recipes.models import Recipe


class RecipeFilter(rest_framework.FilterSet):
    is_favorited = rest_framework.BooleanFilter(method='get_favorite')
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='get_is_in_shopping_cart')

    def get_favorite(self, queryset, value, *args, **kwargs):
        if value:
            return queryset.filter(favourite__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, value, *args, **kwargs):
        if value:
            return queryset.filter(cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'is_in_shopping_cart']
