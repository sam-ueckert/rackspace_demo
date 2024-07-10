from db import vsysdb
from paloaltosdk import PanoramaAPI
import os
from pprint import pprint

vsys_db = vsysdb()

sn = '026701009424_026701009351'
vsys_name = 'CUSTOMERA-VSYS'

# reserved_in_db = vsys_db.reserve_vsys(sn, vsys_name)

# vsys_db.close_connection()
reserved_in_db = True
if reserved_in_db:
    pano = PanoramaAPI()
    pano.IP = os.environ['PANORAMA']
    pano.Username = os.environ['CDWU']
    pano.Password = os.environ['CDWP']
    pano.headers
    pano.login()

    if '_' in sn:
        # this means the HA Pair, find the active to create the vsys
        devices = pano.get_devices()
        found_active_peer = False
        peer_index = -1

        while not found_active_peer and peer_index < 2:
            peer_index += 1

            for device in devices:
            
                if device['@name'] == sn.split('_')[peer_index]:
                    if 'ha' in device:
                        if device['ha']['state'] == 'active':

                            pprint(device['@name'])
                            found_active_peer = True
                            try:
                                resp = pano.create_vsys(vsys_name=vsys_name, vsys_id='auto', serial=device['@name'])
                            
                            continue
                    else:
                        raise Exception("VSYS RESERVE FAILED: Unable to determine HA Active Peer. HA Not present.")
    
     
    #print("Vsys Reserved!")
else:
    print("No VSYS Available to reserve.")