import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from paloaltosdk import PanoramaAPI
from dotenv import load_dotenv
import rackspace_functions as rf

import os
from pprint import pprint

load_dotenv("./.env")





"""
# Rackspace Vsys Dashboard
## Track allocated vsys by firewall

Click on the Data Center at the left to start
"""

@st.cache_resource
def create_local_pano():
    pano = PanoramaAPI()
    pano.IP = os.environ['PANORAMA']
    pano.Username = os.environ['CDWU']
    pano.Password = os.environ['CDWP']
    pano.login()
    return pano

# Local funcions to cache data, using decorator
@st.cache_data
def local_device_data(_pano:PanoramaAPI):
    return pano.get_devices()


@st.cache_data
def local_vsys_data(_pano:PanoramaAPI,devices):
    return pano.get_vsys_data(devices=devices)

#create a cached PanoramaAPI object
pano = create_local_pano()
# get all device data, then pass this data to other functions instead of continuing to query Panorama
all_devices = local_device_data(pano)
all_vsys = local_vsys_data(pano, all_devices)
# st.write(all_vsys)
#### Mock sidebar data
df = pd.read_json('demo_data.json')
df.rename(columns={'data_center_name': 'Data Center'}, inplace=True)
# Create a dropdown menu in the sidebar with the data centers as options
selected_data_center = st.sidebar.selectbox('Select a Data Center', df['Data Center'].unique())
# Filter the DataFrame based on the selected data center
filtered_df = df[df['Data Center'] == selected_data_center]
# Pull the keys out of the zones column, casting it to a list to eliminate PD series object
zones = list(filtered_df['zones'])[0]
# st.dataframe(data = zones, hide_index=True)
selected_zone = st.sidebar.selectbox(f'Select a Zone Within {selected_data_center}', zones)
current_zone = pd.DataFrame(zones[selected_zone])
##### end mock sidebar data

#convert the vsys data to a dataframe
vsys_df = pd.DataFrame(all_vsys)
# Extract hostname and VSYS display name
vsys_display_df = vsys_df.drop(columns=['serial', 'vsys_in_use'])
vsys_display_df.rename(columns={'vsys_max': 'Max Vsys',
                                 'vsys_used': 'Used Vsys',
                                'vsys_free': 'Free Vsys', 
                                'hostname': "Firewall"},
                                inplace=True)
# vsys_display_df['hostname'].pop('serial')
# pprint(vsys_display_df)
# Make selectable rows of firewalss in selected zone
fw_event = st.dataframe(data=vsys_display_df, use_container_width=True, on_select="rerun", hide_index=True, selection_mode="multi-row")
# st.dataframe(data = filtered_df['zones'][0][selected_zone], hide_index=True)

#Create new dataframe with selected firewalls
st.header('Reserve VSYS on selected Firewalls')
fw_selection = fw_event.selection.rows
filtered_df = current_zone.iloc[fw_selection]
if not filtered_df.empty:
    if st.button('Submit'):
        # st.session_state['selected_firewalls'] = filtered_df['firewall_name'].tolist()
        st.rerun()
# st.dataframe(data = filtered_df, hide_index=True)  #TODO add column_config=column_configuration move to new page
