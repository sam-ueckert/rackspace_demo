from paloaltosdk import PanoramaAPI

import os
from pprint import pprint

pano = PanoramaAPI()
pano.IP = os.environ['PANORAMA']
pano.Username = os.environ['CDWU']
pano.Password = os.environ['CDWP']
pano.login()

print(pano.get_sys_limits('026701009351'))