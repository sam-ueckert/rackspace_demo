# THIS CODE PULLS DATA FROM PANORAMA 
from paloaltosdk import PanoramaAPI
import os
from pprint import pprint

pano = PanoramaAPI()

pano.IP = os.environ['PANORAMA']
pano.Username = os.environ['CDWU']
pano.Password = os.environ['CDWP']
pano.headers
pano.login()

available_vsys = pano.get_vsys_data()
pprint(available_vsys)
