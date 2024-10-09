from paloaltosdk.pa_utils import PanoramaAPI
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


resp = pano.create_vsys("RESERVED-test-one", 'auto', "026701009424", tag_name="RESERVED")
print(resp)



pano.commit(target='026701009424')