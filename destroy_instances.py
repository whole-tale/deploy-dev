#!/usr/bin/env python
import json
import requests
import time
import os
import sys
from requests.auth import HTTPBasicAuth

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

api_url = 'https://girder.local.wholetale.org/api/v1'

try:
    r = requests.get(api_url + '/user/authentication', auth=HTTPBasicAuth('admin', 'arglebargle123'))
except:
    print('Girder is no longer running')
    exit()
r.raise_for_status()
headers['Girder-Token'] = r.json()['authToken']['token']

print('Deleting all running instances')
r = requests.get(api_url + '/instance', headers=headers,
                 params={'limit': 0})
r.raise_for_status()
for instance in r.json():
    requests.delete(api_url + '/instance/' + instance['_id'], headers=headers)
