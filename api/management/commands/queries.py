import json
import os

from api.models import GalaxyInstance, Job, JobParam, MetricNumeric, MetricText

from django.core.management.base import BaseCommand
from django.db import transaction, connection


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
    },
    {
        "name": "Top tools, last 4 weeks",
        "path": os.path.join('results', 'tools'),
        "file": 'top_versions_recent.json',
        "query": """
            SELECT
                tool_id, tool_version, count(*) AS count
            FROM api_job
            WHERE create_time >= (now() - '4 week'::interval)
            GROUP BY tooL_id, tool_version
            ORDER BY count desc
        """
    },
    {
        "name": "Top tools, all time",
        "path": os.path.join('results', 'tools'),
        "file": 'top_versions_all.json',
        "query": """
            SELECT
                tool_id, tool_version, count(*) AS count
            FROM api_job
            GROUP BY tool_id, tool_version
            ORDER BY count desc
        """
    },
    {
        "name": "Top tools, all time (no version)",
        "path": os.path.join('results', 'tools'),
        "file": 'top_all.json',
        "query": """
            SELECT
                tool_id, count(tool_id) AS count
            FROM api_job
            GROUP BY tool_id
            ORDER BY count desc
        """
    },
    # {
        # "name": "Top tools, all time (no version)",
        # "path": os.path.join('results', 'tools'),
        # "file": 'top_all.json',
        # "query": """

            # CREATE TEMP TABLE popcon AS
            # SELECT external_job_id, instance_id, count(external_job_id) AS count
            # FROM api_jobparam
            # GROUP BY external_job_id, instance_id
            # ORDER BY count desc;

            # SELECT  popcon.instance_id ,
                    # popcon.external_job_id ,
                    # popcon.count ,
                    # api_job.tool_id
            # FROM    popcon ,
                    # api_job
            # WHERE   popcon.external_job_id = api_job.external_job_id
                    # AND popcon.instance_id = api_job.instance_id
            # ORDER BY count DESC ,
                    # api_job.tool_id DESC;
        # """
    # }
]

class Command(BaseCommand):

    def handle(self, *args, **options):
        for query in QUERIES:
            print("Processing %s" % query['name'])
            if not os.path.exists(query['path']):
                os.makedirs(query['path'])

            with open(os.path.join(query['path'], query['file']), 'w') as handle:
                data = []
                with connection.cursor() as c:
                    c.execute(query['query'])
                    for row in c.fetchall():
                        data.append(row)
                json.dump(data, handle)
