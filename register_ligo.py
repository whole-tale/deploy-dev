import mimetypes
import json
import requests
import os
from requests.auth import HTTPBasicAuth

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
api_url = 'https://girder.local.wholetale.org/api/v1'

try:
    r = requests.get(
        api_url + '/user/authentication', auth=HTTPBasicAuth('admin', 'arglebargle123')
    )
except:
    print('Girder is no longer running')
    exit()
r.raise_for_status()
headers['Girder-Token'] = r.json()['authToken']['token']

ligo_data = [
    "https://www.gw-openscience.org/s/events/GW170104/H-H1_LOSC_4_V1-1167559920-32.hdf5",
    "https://www.gw-openscience.org/s/events/GW170104/GW170104_4_template.hdf5",
    "https://www.gw-openscience.org/s/events/GW150914/GW150914_4_template.hdf5",
    "https://www.gw-openscience.org/s/events/BBH_events_v3.json",
    "https://www.gw-openscience.org/s/events/GW151226/GW151226_4_template.hdf5",
    "https://www.gw-openscience.org/s/events/GW151226/H-H1_LOSC_4_V2-1135136334-32.hdf5",
    "https://www.gw-openscience.org/s/events/LVT151012/L-L1_LOSC_4_V2-1128678884-32.hdf5",
    "https://www.gw-openscience.org/s/events/GW170104/L-L1_LOSC_4_V1-1167559920-32.hdf5",
    "https://www.gw-openscience.org/s/events/LVT151012/LVT151012_4_template.hdf5",
    "https://www.gw-openscience.org/s/events/LVT151012/H-H1_LOSC_4_V2-1128678884-32.hdf5",
    "https://www.gw-openscience.org/s/events/GW150914/H-H1_LOSC_4_V2-1126259446-32.hdf5",
    "https://www.gw-openscience.org/s/events/GW150914/L-L1_LOSC_4_V2-1126259446-32.hdf5",
    "https://www.gw-openscience.org/s/events/GW151226/L-L1_LOSC_4_V2-1135136334-32.hdf5",
]
# r = requests.get(api_url + '/repository/lookup', params={'dataId': json.dumps(ligo_data)})

ligo_dataMap = [
    {
        'dataId': 'https://www.gw-openscience.org/s/events/BBH_events_v3.json',
        'doi': None,
        'name': 'BBH_events_v3.json',
        'repository': 'HTTP',
        'size': 2202,
    },
    {
        'dataId': 'https://www.gw-openscience.org/s/events/GW150914/GW150914_4_template.hdf5',
        'doi': None,
        'name': 'GW150914_4_template.hdf5',
        'repository': 'HTTP',
        'size': 1056864,
    },
    {
        'dataId': 'https://www.gw-openscience.org/s/events/GW151226/GW151226_4_template.hdf5',
        'doi': None,
        'name': 'GW151226_4_template.hdf5',
        'repository': 'HTTP',
        'size': 1056864,
    },
    {
        'dataId': 'https://www.gw-openscience.org/s/events/GW170104/GW170104_4_template.hdf5',
        'doi': None,
        'name': 'GW170104_4_template.hdf5',
        'repository': 'HTTP',
        'size': 1056864,
    },
    {
        'dataId': 'https://www.gw-openscience.org/s/events/GW170104/H-H1_LOSC_4_V1-1167559920-32.hdf5',
        'doi': None,
        'name': 'H-H1_LOSC_4_V1-1167559920-32.hdf5',
        'repository': 'HTTP',
        'size': 1033609,
    },
    {
        'dataId': 'https://www.gw-openscience.org/s/events/GW150914/H-H1_LOSC_4_V2-1126259446-32.hdf5',
        'doi': None,
        'name': 'H-H1_LOSC_4_V2-1126259446-32.hdf5',
        'repository': 'HTTP',
        'size': 1040592,
    },
    {
        'dataId': 'https://www.gw-openscience.org/s/events/LVT151012/H-H1_LOSC_4_V2-1128678884-32.hdf5',
        'doi': None,
        'name': 'H-H1_LOSC_4_V2-1128678884-32.hdf5',
        'repository': 'HTTP',
        'size': 1039648,
    },
    {
        'dataId': 'https://www.gw-openscience.org/s/events/GW151226/H-H1_LOSC_4_V2-1135136334-32.hdf5',
        'doi': None,
        'name': 'H-H1_LOSC_4_V2-1135136334-32.hdf5',
        'repository': 'HTTP',
        'size': 1040336,
    },
    {
        'dataId': 'https://www.gw-openscience.org/s/events/GW170104/L-L1_LOSC_4_V1-1167559920-32.hdf5',
        'doi': None,
        'name': 'L-L1_LOSC_4_V1-1167559920-32.hdf5',
        'repository': 'HTTP',
        'size': 1005007,
    },
    {
        'dataId': 'https://www.gw-openscience.org/s/events/GW150914/L-L1_LOSC_4_V2-1126259446-32.hdf5',
        'doi': None,
        'name': 'L-L1_LOSC_4_V2-1126259446-32.hdf5',
        'repository': 'HTTP',
        'size': 1007420,
    },
    {
        'dataId': 'https://www.gw-openscience.org/s/events/LVT151012/L-L1_LOSC_4_V2-1128678884-32.hdf5',
        'doi': None,
        'name': 'L-L1_LOSC_4_V2-1128678884-32.hdf5',
        'repository': 'HTTP',
        'size': 1018496,
    },
    {
        'dataId': 'https://www.gw-openscience.org/s/events/GW151226/L-L1_LOSC_4_V2-1135136334-32.hdf5',
        'doi': None,
        'name': 'L-L1_LOSC_4_V2-1135136334-32.hdf5',
        'repository': 'HTTP',
        'size': 1022324,
    },
    {
        'dataId': 'https://www.gw-openscience.org/s/events/LVT151012/LVT151012_4_template.hdf5',
        'doi': None,
        'name': 'LVT151012_4_template.hdf5',
        'repository': 'HTTP',
        'size': 1056864,
    },
]

r = requests.post(
    api_url + '/dataset/register',
    params={'dataMap': json.dumps(ligo_dataMap)},
    headers=headers,
)

r = requests.get(
    api_url + '/dataset',
    params={'identifiers': json.dumps(ligo_data)},
    headers=headers,
)
dataSet = [
    {
        'itemId': obj['_id'],
        '_modelType': obj['_modelType'],
        'mountPath': obj['name'],
    }
    for obj in r.json()
]

r = requests.get(api_url + '/image', params={'text': 'Jupyter'}, headers=headers)
imageId = r.json()[0]['_id']

tale = {
    "authors": "Kacper Kowalik",
    "category": "astronomy",
    "config": {},
    "dataSet": dataSet,
    "description": (
        "### LIGO Detected Gravitational Waves from Black Holes\nOn September 14,"
        "2015 at 5:51 a.m. Eastern Daylight Time (09:51 UTC), the twin Laser Inte"
        "rferometer Gravitational-wave Observatory (LIGO) detectors, located in L"
        "ivingston, Louisiana, and Hanford, Washington, USA both measured ripples"
        " in the fabric of spacetime – gravitational waves – arriving at the Eart"
        "h from a cataclysmic event in the distant universe. The new Advanced LIG"
        "O detectors had just been brought into operation for their first observi"
        "ng run when the very clear and strong signal was captured.\n\nThis disco"
        "very comes at the culmination of decades of instrument research and deve"
        "lopment, through a world-wide effort of thousands of researchers, and ma"
        "de possible by dedicated support for LIGO from the National Science Foun"
        "dation. It also proves a prediction made 100 years ago by Einstein that "
        "gravitational waves exist. More excitingly, it marks the beginning of a "
        "new era of gravitational wave astronomy – the possibilities for discover"
        "y are as rich and boundless as they have been with light-based astronomy"
        ".\n\nThis first detection is a spectacular discovery: the gravitational "
        "waves were produced during the final fraction of a second of the merger "
        "of two black holes to produce a single, more massive spinning black hole"
        ". This collision of two black holes had been predicted but never observe"
        "d.\n\nTo learn more about the discovery and the teams that made it possi"
        "ble, view the [**Official Press Release**](https://www.ligo.caltech.edu/"
        "news/ligo20160211) or [**download the PDF**](https://www.ligo.caltech.ed"
        "u/system/media_files/binaries/302/original/detection-press-release.pdf)."
        "To explore how LIGO works run this interactive Tale!\n\nPlease visit htt"
        "ps://gravity.ncsa.illinois.edu/"
    ),
    "icon": (
        "https://raw.githubusercontent.com/whole-tale/jupyter-base/"
        "master/squarelogo-greytext-orangebody-greymoons.png"
    ),
    "illustration": "https://use.yt/upload/e922a8ac",
    "imageId": imageId,
    "public": True,
    "published": False,
    "title": "LIGO Tutorial",
}

r = requests.post(api_url + '/tale', headers=headers, json=tale)
tale = r.json()

params = {'folderId': tale['workspaceId']}
for filepath in ('ligo_tale/LOSC_Event_tutorial.ipynb', 'ligo_tale/readligo.py'):
    filename = os.path.basename(filepath)
    filepath = os.path.abspath(filepath)
    filesize = os.path.getsize(filepath)
    mimeType, _ = mimetypes.guess_type(filepath)
    params = {
        'parentType': 'folder',
        'parentId': tale['workspaceId'],
        'name': filename,
        'size': filesize,
        'mimeType': mimeType,
    }
    r = requests.post(api_url + '/file', params=params, headers=headers)
    obj = r.json()
    r = requests.post(
        api_url + '/file/chunk',
        params={'uploadId': obj['_id'], 'offset': 0},
        headers=headers,
        data=open(filepath, 'rb').read(),
    )
    r.raise_for_status()
