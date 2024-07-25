from paloaltosdk import PanoramaAPI
from db import vsysdb
import os
from pprint import pprint
import json

pano = PanoramaAPI()
vsys_db = vsysdb()

pano.IP = os.environ['PANORAMA']
pano.Username = os.environ['CDWU']
pano.Password = os.environ['CDWP']
pano.headers
pano.login()


resp = pano.delete_vsys("test3", 6, "026701009424")

# with open('asdfasdf.json', 'w') as f:
#     f.write(json.dumps(resp, indent=2))



pano.commit(target='026701009424')
# resp = pano.delete_vsys("test3", 6, "026701009424")

# pano.commit(target='026701009351')
# resp = pano.delete_vsys("test3", 6, "026701009351")