from rest_framework import serializers

from .models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer

    class Meta:
        fields = '__all__'
        model = Recipe
