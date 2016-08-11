from django.core.management.base import BaseCommand, CommandError
from api.models import GalaxyInstance
from django.db import transaction
from django.contrib.auth.models import User
import json

class Command(BaseCommand):
    help = 'Parses geojson file and creates GalaxyInstance objects'

    def add_arguments(self, parser):
        parser.add_argument('geojson', type=open)

    @transaction.atomic
    def handle(self, *args, **options):
        data = json.load(options['geojson'])
        user = User.objects.all()[0]
        for feature in data['features']:
            # {u'geometry': {u'type': u'Point', u'coordinates': [151.2038966,
            # -33.8673176]}, u'type': u'Feature', u'properties': {u'URL':
            # u'https://galaxy-tut.genome.edu.au', u'name': u'Galaxy Tute',
            # u'description': u'Galaxy server for GVL tutorials.'}}
            gi, created = GalaxyInstance.objects.get_or_create(
                humanname=feature['properties']['name'],
                owner=user,
            )
            gi.description = feature['properties']['description']
            if feature['properties']['URL'].startswith('http'):
                gi.url = feature['properties']['URL']

            if 'public' not in gi.tags:
                gi.tags.add('public')
            gi.public = True

            gi.latitude = feature['geometry']['coordinates'][1]
            gi.longitude = feature['geometry']['coordinates'][0]
            gi.save()
