#!/usr/bin/env python
import os
import requests
import sys
import json
import random

GRT_URL = 'http://localhost:8000/grt/'

# First, check status of uploaded data.
galaxy_id = '8a0a34f4-db23-4aa4-84d1-19f490ba0cdf'
api_key = '55692180-3456-468c-a11c-bd5bc943815c'
headers = {
    'AUTHORIZATION': galaxy_id + ':' + api_key,
}
r = requests.post(GRT_URL + 'api/whoami', headers=headers)
data = r.json()
# we get back some information about which reports had previously been uploaded.
remote_reports = data['uploaded_reports']
# so now we can know which to send.
local_reports = [x.strip('.json') for x in os.listdir(sys.argv[1]) if x.endswith('.json')]
for report_id in local_reports:
    if not report_id in remote_reports:
        print("Uploading %s" % report_id)
        files = {
            'meta': open(os.path.join(sys.argv[1], report_id + '.json'), 'rb'),
            'data': open(os.path.join(sys.argv[1], report_id + '.tsv.gz'), 'rb')
        }
        data = {
            'identifier': report_id
        }
        r = requests.post(GRT_URL + 'api/v2/upload', files=files, headers=headers, data=data)
        print(r.json())
