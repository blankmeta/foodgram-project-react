from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    hex_code = models.CharField(max_length=7)
    slug = models.CharField(max_length=200)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.name)
        super().save(force_insert=False, force_update=False, using=None,
                     update_fields=None)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/images/')
    text = models.CharField(max_length=2000)
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeToIngredient',
                                         related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    cooking_time = models.FloatField()
    pub_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-pub_date',)


class RecipeToIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='recipe_ingredients')
    amount = models.FloatField()


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='cart',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='cart',
        on_delete=models.CASCADE,
    )


class Favourite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='favourite',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='favourite',
        on_delete=models.CASCADE
    )
