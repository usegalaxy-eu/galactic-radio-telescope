import json

from api.models import GalaxyInstance, Job, JobParam, MetricNumeric, MetricText

from django.core.management.base import BaseCommand
from django.db import transaction, connection


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('top_all.json', 'w') as handle:
            json.dump(self.top_instances(), handle)


    def top_instances(self):
        # All time
        data = []
        with connection.cursor() as c:
            c.execute('select instance_id, count(instance_id) as count from api_job group by instance_id order by count desc')
            for row in c.fetchall():
                data.append(row)
        return data
