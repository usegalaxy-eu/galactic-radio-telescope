#!/usr/bin/env python
import os
import requests
import sys


GRT_URL = 'http://localhost:8000/grt/'

# First, check status of uploaded data.
galaxy_id = '1'
api_key   = '807c53c2-c02a-4e1a-89b5-f86a86f8c8fa'
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
    if report_id not in remote_reports:
        print("Uploading %s" % report_id)
        files = {
            'meta': open(os.path.join(sys.argv[1], report_id + '.json'), 'rb'),
            'data': open(os.path.join(sys.argv[1], report_id + '.tar.gz'), 'rb')
        }
        data = {
            'identifier': report_id
        }
        r = requests.post(GRT_URL + 'api/v2/upload', files=files, headers=headers, data=data)
        print(r.json())
