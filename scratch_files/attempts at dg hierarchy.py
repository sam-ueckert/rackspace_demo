from paloaltosdk.pa_utils import PanoramaAPI
from db import vsysdb
import os
import json
from pprint import pprint
import rackspace_functions
from panos.panorama import Panorama, DeviceGroup, DeviceGroupHierarchy, OpState

pano = PanoramaAPI()
vsys_db = vsysdb()

pano.IP = settings['PANORAMA']
pano.Username = os.environ['SSO_UNAME']
pano.Password = os.environ['SSO_PW']
# pano.headers
# pano.login()


sdk_pano = Panorama(hostname=settings['PANORAMA'], api_username=os.environ['SSO_UNAME'], api_password=os.environ['SSO_PW'])

# devices = sdk_pano.refresh_devices(expand_vsys=False, include_device_groups=True)



dgs = DeviceGroup.refreshall(sdk_pano)
print(dgs)
# opstate = sdk_pano.OPSTATES
# dg_hierarchy_top = DeviceGroupHierarchy(opstate)
# # opstate.dg_hierachy.fetch()
# # pprint(dg_hierarchy_top.obj)
# for item in dg_hierarchy_top.obj:
#     print(item)
# # dg_hierarchy_top.refresh()
# pprint(f"{opstate.items()}")
# for dg in dgs:
#     pprint(dg)
#     # print(dg.tree())
#     print(dg.OPSTATES)
#     print(dg.xpath())
    
#     # dg.f




# panrest = PanOSAPI(settings['PANORAMA'])
# panrest.IP = settings['PANORAMA']
# panrest.Username = os.environ['SSO_UNAME']
# panrest.Password = os.environ['SSO_PW']
# panrest.headers
# panrest.login()
# print(panrest.sw_version)
# print(pano.get_api_version())
# serial = '026701009351'
# serial = '026701009424'
# # serial = None
# payload = f'''
#             <entry name="Reserved">
#             </entry>
#                 '''
# xpath = f"/config/devices/entry/vsys/entry[@name='vsys3']/tag/entry[@name='NOT_USED-test']=<color>color15</color>"
# xpath = f"/config/devices/entry/vsys/entry"
# device_list=[]
# device_list.append(serial)
# pprint(pano.get_devices(serial=serial))
# device_list = pano.get_devices()
# device_groups = pano.get_devicegroup_members(device_group='GTS-FLEET-V2')
# device_groups = pano.get_devicegroup_members(device_group='GTS-VSYS-IAD')
# with open('device_groups.json', 'w') as f:
    # json.dump(device_groups, f, indent=4)
# pprint(rackspace_functions.create_vsys_reservation(serial, vsys_name='test-tag', devices=device_list, pano=pano))
# xpath = "/config/devices/entry/vsys/entry[@name='vsys6']"
# xpath = "/config/devices/entry/vsys"
# pprint(pano.get_vsys_data())
# # pprint(pano.get_config_xml(xpath, serial))
# action = 'get'
# resp = pano.create_vsys("test3", '6', "026701009424", tag_name="RESERVED")
# with open('xml_to_json.json', 'w') as f:
#     json.dump(pano.config_xml_generic(xpath=xpath, serial=serial, action=action), f, indent=4)
# pano.config_xml_generic(xpath=xpath, serial=serial, action=action)
# pano.commit(target='serial')
# # with open ('response.xml', 'w') as f:
# #     f.write(pano.config_xml_generic(xpath=xpath, serial=serial, action=action))
# xpath = "/config/devices/entry/vsys/entry[@name='vsys6']/tag"
# pprint(pano.config_xml_generic(xpath=xpath, serial=serial))

# tags = panrest.get_tags()
# pprint(tags.reason)
# pano.commit(target='026701009424')
# rackspace_functions.clear_expired_reservations(devices=device_list, pano=pano)
