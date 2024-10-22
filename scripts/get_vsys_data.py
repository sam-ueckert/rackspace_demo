from paloaltosdk.pa_utils import PanoramaAPI
from db import vsysdb
import os
from pprint import pprint
import json

pano = PanoramaAPI()
# vsys_db = vsysdb()

pano.IP = settings['PANORAMA']
pano.Username = os.environ['SSO_UNAME']
pano.Password = os.environ['SSO_PW']
pano.headers
pano.login()


vsys_data = pano.get_vsys_data()
pprint(vsys_data)

with open('vsys_data.json', 'w') as f:
    f.write(json.dumps(vsys_data, indent=2))
# vsys_db.insertdata(vsys_data)
# vsys_db.close_connection()
