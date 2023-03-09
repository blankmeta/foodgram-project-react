from django.db import IntegrityError
from recipes.models import Tag
from .filler import Filler


class Command(Filler):
    @staticmethod
    def _creator(data):
        for tag in data:
            try:
                Tag.objects.get_or_create(name=tag['name'],
                                          color=tag['color'])
                print(f'{tag["name"]} is  successfully created')
            except IntegrityError as e:
                print('Ingredient is already in base.')
