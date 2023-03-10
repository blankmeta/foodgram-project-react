from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Favourite
from recipes.models import ShoppingCart
from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient
from users.models import Subscription
from users.serializers import UserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(),
                                            source='ingredient.id')
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
        model = RecipeIngredient


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = UserSerializer(default=serializers.CurrentUserDefault())
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(many=True,
                                             source='recipe_ingredients')
    is_favorited = serializers.BooleanField(required=False)
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart')

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=request.user,
                                           recipe_id=obj).exists()

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients', 'name', 'image',
            'cooking_time',
            'text',
            'is_favorited',
            'is_in_shopping_cart')
        model = Recipe


class RecipePostSerializer(RecipeSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)

    def create(self, validated_data):
        validated_data.pop('recipe_ingredients')
        tags = validated_data.pop('tags')
        instance = Recipe.objects.create(**validated_data)
        context = self.context['request']

        ingredients = context.data['ingredients']

        objs = []

        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            ingredient = get_object_or_404(Ingredient, id=ingredient_id)
            objs.append(RecipeIngredient(recipe=instance,
                                         ingredient=ingredient,
                                         amount=amount))
        RecipeIngredient.objects.bulk_create(objs)
        instance.tags.set(tags)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipe_ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        objs = []
        for ingredient in ingredients:
            objs.append(RecipeIngredient(
                ingredient=Ingredient.objects.get(
                    id=ingredient['ingredient']['id'].id),
                recipe=instance,
                amount=ingredient['amount']))
        RecipeIngredient.objects.bulk_create(objs)
        instance.save()
        return instance


class FavouriteSerializer(serializers.ModelSerializer):
    def get_is_favorited(self, obj):
        user = self.context.get('request', ).user
        if not user.is_authenticated:
            return False
        return Recipe.objects.filter(favourite__user=user, id=obj.id).exists()

    class Meta:
        fields = ('recipe', 'user')
        model = Favourite


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = ShortRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        read_only_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj).exists()

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
