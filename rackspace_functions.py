from paloaltosdk import PanoramaAPI
import pprint
import toml
import json
import datetime
import os
import pandas as pd
from dotenv import load_dotenv


settings = toml.load("settings.toml")
load_dotenv("./.env")

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



def get_all_reserved_vsys(devices_vsys: list):
    ''' Returns a list of all reserved VSYS on the Panorama. '''
    list_of_reservations = []
    for device in devices_vsys:
        for vsys in device['vsys_in_use']:
            if vsys['display-name'].startswith('RESERVED-'):
                vsys['serial'] = device['serial'].split('_')[0]
                list_of_reservations.append(vsys)
    return list_of_reservations


def find_expired_reservations(list_of_reservations: list):
    '''Finds tags that begin with "RESDATE-" and checks if the date is more than settings['RESERVATION_MAX_DAYS'] days old. '''
    vsys_to_delete = []
    max_reservation_days = settings['RESERVATION_MAX_DAYS']
    today = datetime.datetime.now()

    for reservation in list_of_reservations:
        if 'tags' not in reservation:
            continue
        for tag in reservation['tags']:
            if tag['@name'].startswith('RESDATE:'):
                # Extract the date from the tag name
                res_date_str = tag['@name'].split(':')[1]
                res_date = datetime.datetime.strptime(res_date_str, "%Y-%m-%d")
                
                # Calculate the expiration date
                expiration_date = res_date + datetime.timedelta(days=max_reservation_days)
                
                # Compare the reservation date to the expiration date
                if expiration_date < today:
                    vsys_to_delete.append(reservation)
                    break  # No need to check other tags for this reservation

    return vsys_to_delete
    
    
def clear_expired_reservations(devices:list, pano:PanoramaAPI):
    ''' Clears expired reservations from the Panorama. '''
    devices_vysy = pano.get_vsys_data(devices=devices)
    list_of_reservations = get_all_reserved_vsys(devices_vysy)
    with open('reserved.json', 'w') as f:
        f.write(json.dumps(list_of_reservations, indent=2))
    # flagged_for_deletion = check_vsys_reservation_date(list_of_reservations)
    flagged_for_deletion = find_expired_reservations(list_of_reservations)
    for vsys in flagged_for_deletion:
        try:
            resp = pano.delete_vsys(serial=vsys['serial'], vsys_name=vsys['@name'])
            print(resp)
            pano.commit(target=vsys['serial'])
        except Exception as e:
            print(e)
    
     
def create_batch_vsys_reservations(reservations:pd.DataFrame, devices:list):
    ''' Creates a batch of VSYS reservations on the Panorama. Creates new pano connection for writes, instead of reusing app connection.'''
    max_reservation_days = settings['RESERVATION_MAX_DAYS']
    reservation_prefix = settings['RESERVATION_PREFIX']
    today = datetime.datetime.now()
    # Set the expiration date to the max reservation (set in .toml file) days from today
    expiration_date = (today + datetime.timedelta(days=max_reservation_days)).strftime('%Y-%d-%m')
    pano = PanoramaAPI()
    pano.IP = os.environ['PANORAMA']
    pano.Username = os.environ['CDWU']
    pano.Password = os.environ['CDWP']
    try:
        pano.login()
    except Exception as e:
        print('Failed to login to Panorama')
        pano.logger.error(e)
    
    for index, device in reservations.iterrows():
        # Create vysy, using the name prefix and the expiration date
        serial = device['serial'].split('_')[0]
        print(f"Creating VSYS: {device['Reserved Vsys ID']}_{expiration_date} on {serial}")
        resp = pano.create_vsys(vsys_name=f"RES_{device['Reserved Vsys ID']}_{expiration_date}", vsys_id='auto', serial=serial)
        print(resp)
        pano.commit(target=serial)
    return resp
            