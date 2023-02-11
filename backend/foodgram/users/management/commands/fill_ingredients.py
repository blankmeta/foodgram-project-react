from django.db import IntegrityError
from recipes.models import Ingredient
from .filler import Filler


class Command(Filler):
    @staticmethod
    def _creator(data):
        for ingredient in data:
            try:
                Ingredient.objects.get_or_create(name=ingredient['name'],
                                                 measurement_unit=ingredient['measurement_unit'])
                print(f'{ingredient["name"]} is  successfully created')
            except IntegrityError as e:
                print('Ingredient is already in base.')
