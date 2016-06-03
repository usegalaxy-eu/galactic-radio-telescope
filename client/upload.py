import requests
import json
import random

GRT_URL = 'http://localhost:8000/grt/api/v1/upload'
payload = {
    'meta': {
        'instance_uuid': '8bdea9afb91142ffb4e9eb8df3f4ee25',
        'instance_api_key': '8bdea9afb91142ffb4e9eb8df3f4ee25',
        'total_users': 80,
        # Statistics are sent weekly.
        'active_users': random.randint(0, 80),
        'recent_jobs': random.randint(0, 1000),
    },
    'tools': [
        {
            'tool_id': 'xmfa2tbl',
            'tool_version': '2.4.0.0',
            'tool_name': 'Convert XMFA to a percent identity table',
        }
    ],
    'jobs': [
        {# A single job
            'tool': 0, # Index in tools array.
            'date': 1464978266,
            'metrics': {
                'cpuinfo_cores_allocated': 1,
                'core_runtime_seconds': random.randint(2, 50),
            },
            # We do not currently accept/process parameters. TODO.
        }
    ]
}

r = requests.post(GRT_URL, data=json.dumps(payload))
print r
print r.text
