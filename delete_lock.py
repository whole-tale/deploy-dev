#!/usr/bin/python
import json
import requests
import time
import os
import sys

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

api_url = 'https://girder.local.wholetale.org/api/v1'
datasetId = 'https://publish.globus.org/jspui/handle/ITEM/113'


if not 'GIRDER_TOKEN' in os.environ:
    print('Error: GIRDER_TOKEN is not set')
    exit(2)

girderToken = os.environ['GIRDER_TOKEN']

print('Girder Token: >%s<' % girderToken)

# Store token for future requests
headers['Girder-Token'] = girderToken

lockId = sys.argv[1]

r = requests.delete(api_url + '/dm/lock/' + lockId, headers=headers)
r.raise_for_status()
