from paloaltosdk import PanoramaAPI
from db import vsysdb
import os
import json
from pprint import pprint

pano = PanoramaAPI()
vsys_db = vsysdb()

pano.IP = os.environ['PANORAMA']
pano.Username = os.environ['CDWU']
pano.Password = os.environ['CDWP']
pano.headers
pano.login()


# serial = '026701009351'
serial = '026701009424'
# serial = None
payload = f'''
            <entry name="NOT_USED">
            <color>color15</color>
            </entry>
                '''
# xpath = f"/config/devices/entry/vsys/entry[@name='vsys3']/tag/entry[@name='NOT_USED-test']=<color>color15</color>"
# xpath = f"/config/devices/entry/vsys/entry"
xpath = "/config/devices/entry/vsys/entry[@name='vsys6']"
# # pprint(pano.get_config_xml(xpath, serial))
action = 'get'
# with open('xml_to_json.json', 'w') as f:
#     json.dump(pano.config_xml_generic(xpath=xpath, serial=serial, action=action), f, indent=4)
# pano.commit(target='serial')
# # with open ('response.xml', 'w') as f:
# #     f.write(pano.config_xml_generic(xpath=xpath, serial=serial, action=action))
# xpath = "/config/devices/entry/vsys/entry[@name='vsys6']/tag"
pprint(pano.config_xml_generic(xpath=xpath, serial=serial))
