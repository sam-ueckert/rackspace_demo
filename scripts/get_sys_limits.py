from paloaltosdk.pa_utils import PanoramaAPI

import os
from pprint import pprint

pano = PanoramaAPI()
pano.IP = settings['PANORAMA']
pano.Username = os.environ['SSO_UNAME']
pano.Password = os.environ['SSO_PW']
pano.login()

print(pano.get_sys_limits('026701009351'))
