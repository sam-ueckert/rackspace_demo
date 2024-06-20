# THIS CODE PULLS DATA FROM PANORAMA 
from paloaltosdk import PanoramaAPI
import os

pano = PanoramaAPI()

pano.IP = os.environ['PANORAMA']
pano.Username = os.environ['CDWU']
pano.Password = os.environ['CDWP']
pano.headers
pano.login()

available_vsys = pano.get_available_vsys("026701009424")
print(available_vsys)

