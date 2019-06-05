#!/usr/bin/env python
import json
import pprint
import sseclient
import sys
import time

token = sys.argv[1]
def with_urllib3(url):
    """Get a streaming response for the given event feed using urllib3."""
    import urllib3
    http = urllib3.PoolManager()
    return http.request('GET', url, preload_content=False)

def with_requests(url):
    """Get a streaming response for the given event feed using requests."""
    import requests
    headers = {'Girder-Token': token}
    return requests.get(url, stream=True, headers=headers)

t = int(time.time())
url = 'https://girder.local.wholetale.org/api/v1/notification/stream?since={}'.format(t)
response = with_requests(url)
client = sseclient.SSEClient(response)
for event in client.events():
    data = json.loads(event.data)
    if (data['type'] == 'wt_progress'):
        pprint.pprint(data)
