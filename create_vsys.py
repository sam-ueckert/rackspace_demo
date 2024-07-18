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


resp = pano.create_vsys("test3", '6', "026701009424")
print(resp)



pano.commit(target='026701009424')