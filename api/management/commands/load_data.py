from django.core.management.base import BaseCommand, CommandError
from api.models import GalaxyInstance
from django.db import transaction
from django.contrib.auth.models import User
import json

class Command(BaseCommand):
    help = 'Load data from a Galaxy data directory.'

    def add_arguments(self, parser):
        parser.add_argument('directory')

    @transaction.atomic
    def handle(self, *args, **options):
        data_dir = json.load(options['directory'])
        print(data_dir)
