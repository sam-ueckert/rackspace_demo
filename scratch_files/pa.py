# THIS CODE PULLS DATA FROM PANORAMA 
from paloaltosdk import PanoramaAPI
import os
from pprint import pprint

pano = PanoramaAPI()

pano.IP = settings['PANORAMA']
pano.Username = os.environ['SSO_UNAME']
pano.Password = os.environ['SSO_PW']
pano.headers
pano.login()

available_vsys = pano.get_vsys_data()
pprint(available_vsys)
