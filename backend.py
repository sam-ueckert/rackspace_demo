# THIS CODE PULLS DATA FROM PANORAMA 
from paloaltosdk import PanoramaAPI
from db import vsysdb
import os
from pprint import pprint

pano = PanoramaAPI()
vsys_db = vsysdb()

pano.IP = os.environ['PANORAMA']
pano.Username = os.environ['CDWU']
pano.Password = os.environ['CDWP']
pano.headers
pano.login()

vsys_data = pano.get_vsys_data()
pprint(vsys_data)




