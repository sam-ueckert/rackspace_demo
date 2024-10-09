from paloaltosdk import PanoramaAPI
import rackspace_functions as rf
import pprint
import toml
import json
import datetime
import os
import pandas as pd
from dotenv import load_dotenv


settings = toml.load("settings.toml")
load_dotenv("./.env")
search_dgs = settings['DEVICE_GRPS']

# settings = toml.load("settings.toml")
# from panos.panorama import Panorama, DeviceGroup, DeviceGroupHierarchy, OpState

pano = PanoramaAPI()
# vsys_db = vsysdb()

pano.IP = os.environ['PANORAMA']
pano.Username = os.environ['CDWU']
pano.Password = os.environ['CDWP']
# pano.headers
pano.login()

# Local funcions to cache data, using decorator
def local_device_data(_pano: PanoramaAPI):
    return pano.get_devices()


def local_vsys_data(_pano: PanoramaAPI, devices):
    return pano.get_vsys_data(devices=devices)


def get_local_data(pano: PanoramaAPI, dg_list: list):
    '''Retrieves all devices and vysys data from Panorama'''
    all_devices = local_device_data(pano)
    filtered_serials = rf.get_serials_from_dgs(pano, dg_list)
    in_scope_devices = rf.filter_devices_by_serial(all_devices, filtered_serials)
    all_vsys = local_vsys_data(pano, in_scope_devices)
    return all_devices, all_vsys, in_scope_devices


all_devices, all_vsys, in_scope_devices = get_local_data(pano, settings['DEVICE_GRPS'])

pass
# panrest = PanOSAPI(os.environ['PANORAMA'])
# panrest.IP = os.environ['PANORAMA']
# panrest.Username = os.environ['CDWU']
# panrest.Password = os.environ['CDWP']
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
