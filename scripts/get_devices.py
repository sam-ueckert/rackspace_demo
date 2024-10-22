from paloaltosdk.pa_utils import PanoramaAPI
import json

import os

pano = PanoramaAPI()
pano.IP = settings['PANORAMA']
pano.Username = os.environ['SSO_UNAME']
pano.Password = os.environ['SSO_PW']
pano.login()

devices = pano.get_devices()
with open('json/devices.json', 'w') as f:
    f.write(json.dumps(devices, indent=2))
