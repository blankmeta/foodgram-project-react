from django_filters import rest_framework
from django_filters.rest_framework import filters

from recipes.models import Recipe, Tag, Ingredient


class RecipeFilter(rest_framework.FilterSet):
    is_favorited = rest_framework.BooleanFilter(method='get_favorite')
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='get_is_in_shopping_cart')
    tags = filters.ModelMultipleChoiceFilter(field_name='tags__slug',
                                             to_field_name='slug',
                                             queryset=Tag.objects.all())

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
        fields = ('tags', 'is_favorited', 'is_in_shopping_cart')


class IngredientFilter(rest_framework.FilterSet):
    name = rest_framework.CharFilter(method='get_name')

    def get_name(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(name__istartswith=value)

    class Meta:
        model = Ingredient
        fields = ('name',)