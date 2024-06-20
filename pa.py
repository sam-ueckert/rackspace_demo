# THIS CODE PULLS DATA FROM PANORAMA 


from paloaltosdk import PanoramaAPI
import os

pano = PanoramaAPI()

pano.IP = ''
pano.Username = os.environ['CDWU']
pano.Password = os.environ['CDWP']
pano.headers
pano.login()

print(pano.get_devicegroups())