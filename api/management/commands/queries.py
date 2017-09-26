import json
import os
import numpy

from django.core.management.base import BaseCommand
from django.db import connection

RECENT = """WHERE create_time >= (now() - '4 week'::interval)"""


def top_exec_versions_recent(c):
    return top_exec_versions_all(c, time_filter=RECENT)


def top_exec_versions_all(c, time_filter=""):
    c.execute(
        """
            SELECT
                tool_id, tool_version, count(*) AS count
            FROM api_job
            {time_filter}
            GROUP BY tool_id, tool_version
            ORDER BY count desc
        """.format(time_filter=time_filter)
    )
    data = {}
    for row in c.fetchall():
        if row[0] not in data:
            data[row[0]] = {}

        data[row[0]][row[1]] = row[2]

    for key in data.keys():
        val = sum((data[key][k] for k in data[key].keys()))
        data[key]['_sum'] = val
    return data


def top_inst_versions_recent(c):
    return top_inst_versions_all(c, time_filter=RECENT)


def top_inst_versions_all(c, time_filter=""):
    c.execute(
        """
        SELECT tool_id,
               count(tool_id) AS count

            FROM (
                SELECT tool_id
                FROM api_job
                {time_filter}
                GROUP BY tool_id, instance_id
                ORDER by tool_id
            )
        AS tmp group by tool_id;
        """.format(time_filter=time_filter)
    )
    data = {}
    for row in c.fetchall():
        if row[0] not in data:
            data[row[0]] = {}

        data[row[0]] = row[1]
    return data


def runtimes(c):
    # First we collect a list of tools.
    print(' locating tools')
    c.execute("""
        SELECT
            api_job.tool_id,
            api_job.tool_version
        FROM api_job
        GROUP BY
            api_job.tool_id,
            api_job.tool_version
        ORDER BY
            api_job.tool_id asc,
            api_job.tool_version asc
    """)
    tools = []
    for row in c.fetchall():
        tools.append((row[0], row[1]))

    print(' locating instances')
    # Next we collect a list of instances.
    c.execute("""
        SELECT id FROM api_galaxyinstance;
    """)
    instances = list([x[0] for x in c.fetchall()])

    print(' mxn')
    # Last, we iterate over them.
    for instance in instances:
        for (tool_id, tool_version) in tools:
            c.execute("""
                SELECT
                    api_metricnumeric.value
                FROM
                    api_metricnumeric, api_job
                WHERE
                    api_metricnumeric.external_job_id = api_job.external_job_id AND
                    api_job.tool_id = %s AND
                    api_job.tool_version = %s AND
                    api_job.state = 'ok' AND
                    api_metricnumeric.name = 'runtime_seconds' AND
                    api_job.instance_id = %s
                ;
            """, (tool_id, tool_version, instance))
            points = []
            for row in c.fetchall():
                points.append(int(row[0]))

            if len(points) == 0:
                continue

            # Remove any slashes.
            tool_id = tool_id.replace('/', '_')

            # Aggregate/histogram of points.
            (hist, bin_edges) = numpy.histogram(points)
            data = list(zip(
                map(int, bin_edges),
                map(int, hist)
            ))
            yield (instance, tool_id, tool_version, data)


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
                api_galaxyinstance.url AS url,
                top_instances.count AS count
            FROM top_instances, api_galaxyinstance
            WHERE top_instances.instance_id = api_galaxyinstance.id;
        """
    },
    {
        "name": "Top tools, all time (no version)",
        "path": os.path.join('results', 'tools'),
        "file": 'top_all.json',
        "table": False,
        "query": """
            SELECT
                tool_id, count(tool_id) AS count
            FROM api_job
            GROUP BY tool_id
            ORDER BY count desc
        """
    },
]

COMPLEX_QUERIES = [
    {
        "name": "Top executed tools, last 4 weeks",
        "path": os.path.join('results', 'tools'),
        "file": 'top_exec_versions_recent.json',
        "query": top_exec_versions_recent
    },
    {
        "name": "Top executed tools, all time",
        "path": os.path.join('results', 'tools'),
        "file": 'top_exec_versions_all.json',
        "query": top_exec_versions_all
    },
    {
        "name": "Top installed tools, last 4 weeks",
        "path": os.path.join('results', 'tools'),
        "file": 'top_inst_versions_recent.json',
        "query": top_inst_versions_recent
    },
    {
        "name": "Top installed tools, all time",
        "path": os.path.join('results', 'tools'),
        "file": 'top_inst_versions_all.json',
        "query": top_inst_versions_all
    },
    {
        "name": "Tool runtimes (per-instance)",
        "path": os.path.join('results', 'tools', 'runtimes', '{instance}'),
        "file": '{tool_id}--{tool_version}.json',
        "per_instance_tool": True,
        "query": runtimes
    },
]


class Command(BaseCommand):

    def write_file(self, query, data, name=None):
        fn = os.path.join(query['path'], query['file'])
        if name:
            fn = name
        with open(fn, 'w') as handle:
            json.dump(data, handle)

    def _tabular_data(self, query):
        with connection.cursor() as c:
            c.execute(query['query'])
            if query['table']:
                data = []
                column_names = [col[0] for col in c.description]
                for idx, row in enumerate(c.fetchall()):
                    data.append(dict(zip(column_names, row)))
                self.write_file(query, data)

    def _dict_data(self, query):
        with connection.cursor() as c:
            c.execute(query['query'])
            data = {}
            column_names = [col[0] for col in c.description]
            if len(column_names) == 2:
                for row in c.fetchall():
                    data[row[0]] = row[1]
            else:
                for row in c.fetchall():
                    data[row[0]] = dict(zip(
                        column_names[1:], row[1:]))
            self.write_file(query, data)

    def _simple_complex_query(self, query):
        if not os.path.exists(query['path']):
            os.makedirs(query['path'])

        with connection.cursor() as c:
            data = query['query'](c)
            self.write_file(query, data)

    def _complex_complex_query(self, query):
        with connection.cursor() as c:
            for (instance, tool_id, tool_version, data) in query['query'](c):
                kwargs = {'instance': instance, 'tool_id': tool_id, 'tool_version': tool_version}
                dirname = query['path'].format(**kwargs)
                if not os.path.exists(dirname):
                    os.makedirs(dirname)
                self.write_file(query, data, name=os.path.join(dirname, query['file'].format(**kwargs)))

    def handle(self, *args, **options):
        for query in QUERIES:
            print("Processing %s" % query['name'])
            if not os.path.exists(query['path']):
                os.makedirs(query['path'])

            if query['table']:
                self._tabular_data(query)
            else:
                self._dict_data(query)

        for query in COMPLEX_QUERIES:
            print("Processing %s" % query['name'])
            if 'per_instance_tool' in query:
                self._complex_complex_query(query)
            else:
                self._simple_complex_query(query)
