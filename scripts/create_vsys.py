from paloaltosdk.pa_utils import PanoramaAPI
from db import vsysdb
import os
from pprint import pprint
import json

pano = PanoramaAPI()
vsys_db = vsysdb()

pano.IP = settings['PANORAMA']
pano.Username = os.environ['SSO_UNAME']
pano.Password = os.environ['SSO_PW']
pano.headers
pano.login()


resp = pano.create_vsys("RESERVED-test-one", 'auto', "026701009424", tag_name="RESERVED")
print(resp)



pano.commit(target='026701009424')