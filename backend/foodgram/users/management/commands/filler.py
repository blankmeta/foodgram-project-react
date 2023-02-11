import json
import os
from abc import abstractmethod

from django.conf import settings
from django.core.management import BaseCommand, CommandError

DATA_DIRECTORY_NAME = 'data'

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Filler(BaseCommand):
    @staticmethod
    @abstractmethod
    def _creator(data):
        pass

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('json_name', nargs='+', type=str)

    def handle(self, *args, **options):
        json_path = DATA_ROOT
        try:
            with open(os.path.join(DATA_ROOT, ''.join(options['json_name'])), 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                self._creator(json_data)
        except FileNotFoundError:
            raise CommandError(f'File does not exist.\n'
                               f'{os.listdir(json_path)} are available')
