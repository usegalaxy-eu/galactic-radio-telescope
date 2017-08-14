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
        "table": False,
        "query": """
            CREATE TEMP TABLE top_instances AS
            SELECT
                instance_id, count(instance_id) AS count
            FROM api_job
            GROUP BY instance_id
            ORDER BY count DESC;

            SELECT
                api_galaxyinstance.url AS url,
                top_instances.count AS count
            FROM top_instances, api_galaxyinstance
            WHERE top_instances.instance_id = api_galaxyinstance.id;
        """
    },
    {
        "name": "Top instances, last 4 weeks",
        "path": os.path.join('results', 'instance'),
        "file": 'top_recent.json',
        "table": False,
        "query": """
            CREATE TEMP TABLE top_recent_instances AS
            SELECT
                instance_id, count(instance_id) AS count
            FROM api_job
            WHERE create_time >= (now() - '4 week'::interval)
            GROUP BY instance_id
            ORDER BY count desc;

            SELECT
                top_instances.count AS count,
                api_galaxyinstance.url AS url,
                api_galaxyinstance.id as id
            FROM top_instances, api_galaxyinstance
            WHERE top_instances.instance_id = api_galaxyinstance.id;
        """
    },
    {
        "name": "Top tools, last 4 weeks",
        "path": os.path.join('results', 'tools'),
        "file": 'top_versions_recent.json',
        "table": True,
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
        "table": True,
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
        "table": True,
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
                with connection.cursor() as c:
                    c.execute(query['query'])
                    if query['table']:
                        data = []
                        column_names = [col[0] for col in c.description]
                        for row in c.fetchall():
                            data.append(dict(zip(column_names, row)))
                    else:
                        data = {}
                        column_names = [col[0] for col in c.description]
                        for row in c.fetchall():
                            data[row[0]] = dict(zip(column_names[1:], row[1:]))

                json.dump(data, handle)
