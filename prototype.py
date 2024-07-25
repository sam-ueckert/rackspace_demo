from paloaltosdk import PanoramaAPI, PanOSAPI
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

panrest = PanOSAPI(os.environ['PANORAMA'])
panrest.IP = os.environ['PANORAMA']
panrest.Username = os.environ['CDWU']
panrest.Password = os.environ['CDWP']
panrest.headers
panrest.login()
print(panrest.sw_version)
print(pano.get_api_version())
# serial = '026701009351'
serial = '026701009424'
# serial = None
payload = f'''
            <entry name="Reserved">
            <color>color15</color>
            </entry>
                '''
# xpath = f"/config/devices/entry/vsys/entry[@name='vsys3']/tag/entry[@name='NOT_USED-test']=<color>color15</color>"
# xpath = f"/config/devices/entry/vsys/entry"
device_list=[]
device_list.append(serial)
pprint(pano.get_devices(serial=serial))
xpath = "/config/devices/entry/vsys/entry[@name='vsys6']"
# pprint(pano.get_vsys_data())
# # pprint(pano.get_config_xml(xpath, serial))
# action = 'get'
# resp = pano.create_vsys("test3", '6', "026701009424", tag_name="RESERVED")
# with open('xml_to_json.json', 'w') as f:
#     json.dump(pano.config_xml_generic(xpath=xpath, serial=serial, action=action), f, indent=4)
# pano.commit(target='serial')
# # with open ('response.xml', 'w') as f:
# #     f.write(pano.config_xml_generic(xpath=xpath, serial=serial, action=action))
# xpath = "/config/devices/entry/vsys/entry[@name='vsys6']/tag"
# pprint(pano.config_xml_generic(xpath=xpath, serial=serial))

# tags = panrest.get_tags()
# pprint(tags.reason)
