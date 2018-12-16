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

# Get user ID
r = requests.get(api_url + '/user/me', headers=headers)
r.raise_for_status()
userInfo = r.json()
userId = userInfo['_id']

print('User ID: %s' % userId)

# Get ID of Data folder
r = requests.get(api_url + '/folder?name=Data&parentId=%s&parentType=user&reload=true' % userId, 
                  headers=headers)
r.raise_for_status()
dataFolder = r.json()[0]
dataFolderId = dataFolder['_id']

print('Data folder ID: %s' % dataFolderId)

# Lookup dataset
r = requests.get(api_url + '/repository/lookup', params={'dataId': json.dumps([datasetId])}, 
                 headers=headers)
r.raise_for_status()
dataMap = r.json()
print('DataMap: %s' % dataMap)

# Check if already imported
def findNameInList(lst, name, idField):
    for obj in lst:
        if obj['name'] == name:
            return obj[idField]
    return None
    
def findNameInListing(parentFolderId, name, idField):
    r = requests.get(api_url + '/folder/%s/listing' % parentFolderId, headers=headers)
    print(r.json())
    folderId = findNameInList(r.json()['folders'], name, idField)
    if folderId is not None:
        return folderId
    return findNameInList(r.json()['files'], name, idField)

dataSetId = findNameInListing(dataFolderId, dataMap[0]['name'], '_id')

if dataSetId is None:
    # If not, import it
    print('Importing dataset')
    params = {
        'parentId': dataFolderId,
        'parentType': 'folder',
        'dataMap': json.dumps(dataMap),
    }

    r = requests.post(api_url + '/dataset/register', params=params, headers=headers)
    r.raise_for_status()
    
    print(r.text)
    dataSetId = findNameInListing(dataFolderId, dataMap[0]['name'], '_id')
else:
    print('Dataset already imported')

# Get id of small file that should always be there
fileId = findNameInListing(dataSetId, 'globus_metadata.json', 'itemId')
print('File ID: %s' % fileId)

# Create a session
dataSet = [{'itemId': fileId, 'mountPath': '/file'}]
r = requests.post(api_url + '/dm/session', params={'dataSet': json.dumps(dataSet)}, 
                  headers=headers)
r.raise_for_status()
sessionId = r.json()['_id']
print('Session ID: %s' % sessionId)

try:
    # Lock the file
    r = requests.post(api_url + '/dm/lock', params={'sessionId': sessionId, 'itemId': fileId},
                      headers=headers)
    r.raise_for_status()
    print(r.text)
    lockId = r.json()['_id']
    
    time.sleep(2)
    r = requests.delete(api_url + '/dm/lock/' + lockId, headers=headers)
    r.raise_for_status()
finally:
    # Delete the session when done
    r = requests.delete(api_url + '/dm/session/' + sessionId, headers=headers)
    r.raise_for_status()

print('Done')