from paloaltosdk.pa_utils import PanoramaAPI
import json

import os

pano = PanoramaAPI()
pano.IP = os.environ['PANORAMA']
pano.Username = os.environ['CDWU']
pano.Password = os.environ['CDWP']
pano.login()

devices = pano.get_devices()
with open('json/devices.json', 'w') as f:
    f.write(json.dumps(devices, indent=2))
