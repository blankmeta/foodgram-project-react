from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.new_fields import Base64ImageField
from .models import Tag, Ingredient, Recipe, RecipeToIngredient
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeToIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), source='ingredient.id')
    name = serializers.CharField(
        read_only=True,
        source='ingredient.name'
    )
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredient.measurement_unit'
    )

    class Meta:
        fields = ('id', 'amount', 'name', 'measurement_unit')
        model = RecipeToIngredient


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = UserSerializer(default=serializers.CurrentUserDefault())
    ingredients = RecipeToIngredientSerializer(many=True, source='recipe_ingredients')

    def create(self, validated_data):
        ingredients = validated_data.pop('recipe_ingredients')
        tags = validated_data.pop('tags')
        instance = Recipe.objects.create(**validated_data)
        context = self.context['request']

        ingredients = context.data['ingredients']

        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            ingredient = get_object_or_404(Ingredient, id=ingredient_id)
            RecipeToIngredient.objects.create(recipe=instance,
                                              ingredient=ingredient,
                                              amount=amount)
        instance.tags.set(tags)
        return instance

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'cooking_time', 'text', 'cooking_time',)
        model = Recipe
