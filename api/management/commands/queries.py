import json
import os
import logging

from api.models import GalaxyInstance, Job, JobParam, MetricNumeric, MetricText

from django.core.management.base import BaseCommand
from django.db import transaction, connection


logger = logging.getLogger(__name__)
QUERIES = [
    {
        "name": "Top instances, all time",
        "path": os.path.join('results', 'instance'),
        "file": 'top_all.json',
        "query": """
            SELECT
                instance_id, count(instance_id) AS count
            FROM api_job
            GROUP BY instance_id
            ORDER BY count desc
        """
    },
    {
        "name": "Top instances, last 4 weeks",
        "path": os.path.join('results', 'instance'),
        "file": 'top_recent.json',
        "query": """
            SELECT
                instance_id, count(instance_id) AS count
            FROM api_job
            WHERE create_time >= (now() - '4 week'::interval)
            GROUP BY instance_id
            ORDER BY count desc
        """
    }
]

class Command(BaseCommand):

    def handle(self, *args, **options):
        for query in QUERIES:
            logging.info("Processing %s", query['name'])
            if not os.path.exists(query['path']):
                os.makedirs(query['path'])

            with open(os.path.join(query['path'], query['file']), 'w') as handle:
                data = []
                with connection.cursor() as c:
                    c.execute(query['query'])
                    for row in c.fetchall():
                        data.append(row)
                json.dump(data, handle)
