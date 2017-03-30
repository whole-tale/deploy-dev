import json
import requests
import time

params = {
    'login': 'admin',
    'email': 'root@dev.null',
    'firstName': 'John',
    'lastName': 'Doe',
    'password': 'arglebargle123',
    'admin': True
}
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
api_url = 'http://localhost:8080/api/v1'

# Create Admin user
r = requests.post(api_url + '/user', params=params, headers=headers)
r.raise_for_status()

# Store token for future requests
headers['Girder-Token'] = r.json()['authToken']['token']

# Enable ytHub plugin
r = requests.put(api_url + '/system/plugins', headers=headers,
                 params={'plugins': json.dumps(['ythub'])})
r.raise_for_status()

# Restart is required to load the plugin
r = requests.put(api_url + '/system/restart', headers=headers)
r.raise_for_status()

# Give girder time to restart
print('Sleeping...')
time.sleep(12)

# generate keys
r = requests.post(api_url + '/ythub/genkey', headers=headers)
r.raise_for_status()
keys = r.json()

# Set ythub plugin
settings = [
    {
        'key': 'ythub.tmpnb_url',
        'value': 'http://proxy:8000/'
    }, {
        'key': 'ythub.culling_period',
        'value': '4'
    }, {
        'key': 'ythub.culling_frequency',
        'value': '4'
    }, {
        'key': 'ythub.priv_key',
        'value': keys['ythub.priv_key']
    }, {
        'key': 'ythub.pub_key',
        'value': keys['ythub.pub_key']
    }
]

r = requests.put(api_url + '/system/setting', headers=headers,
                 params={'list': json.dumps(settings)})
r.raise_for_status()

# Create default assetstore
r = requests.post(api_url + '/assetstore', headers=headers,
                  params={'type': 0, 'name': 'test', 'root': '/tmp/girder'})

# Create default frontend
frontend = {
    "command": ("jupyter notebook --no-browser --port {port} --ip=0.0.0.0 "
                "--NotebookApp.token={token} "
                "--NotebookApp.base_url=/{base_path} " 
                "--NotebookApp.port_retries=0"),
    "description": "Run Jupyter Notebook",
    "imageName": "xarthisius/ythub-jupyter",
    "memLimit": "1024m",
    "port": "8888",
    "public": True,
    "user": "jovyan"
}

r = requests.post(api_url + '/frontend', headers=headers,
                  params=frontend)

# Create test data structure
r = requests.post(api_url + '/collection', headers=headers,
                  params={'name': 'test',
                          'description': 'test collection',
                          'public': True})
r.raise_for_status()
coll = r.json()

r = requests.post(api_url + '/folder', headers=headers,
                  params={'parentType': 'collection',
                          'parentId': coll['_id'],
                          'name': 'test',
                          'public': True})
r.raise_for_status()
folder = r.json()

print('You should be all set!!')
print('try going to http://localhost:8080 and log in with: ')
print('user : %s' % params['login'])
print('pass : %s' % params['password'])
