from paloaltosdk import PanoramaAPI
import pprint
import toml

settings = toml.load("settings.toml")

def create_vsys_reservation(sn:str, vsys_name:str, devices:list, pano:PanoramaAPI):
    ''' Creates a VSYS reservation on the Panorama, taging the VSYS as RESERVED and prefixing the name with RESERVED-.'''
    if '_' in sn:
        # this means the HA Pair, find the active to create the vsys
        # devices = pano.get_devices()
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
                                resp = pano.create_vsys(vsys_name=f"RESERVED-{vsys_name}", vsys_id='auto', serial=device['@name'], tag_name='RESERVED')
                            
                            except Exception as e:
                                print(e)
                                return None
                    else:
                        raise Exception("VSYS RESERVE FAILED: Unable to determine HA Active Peer. HA Not present.")
    else:
        # this means the device is a single device
        for device in devices:
            if device['@name'] == sn:
                try:
                    resp = pano.create_vsys(vsys_name=f"RESERVED-{vsys_name}", vsys_id='auto', serial=device['@name'], tag_name='RESERVED')
                except Exception as e:
                    print(e)
                    return None
    return resp


def clear_expired_reservations(devices:list, pano:PanoramaAPI):
    ''' Clears expired reservations from the Panorama. '''
    for device in devices:
        if 
     
