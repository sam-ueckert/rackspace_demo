import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from paloaltosdk import PanoramaAPI
from dotenv import load_dotenv

import os
from pprint import pprint

load_dotenv("./.env")





"""
# Rackspace Vsys Dashboard
## Track allocated vsys by firewall

Click on the Data Center at the left to start
"""

@st.cache_data
def get_vsys_data(pano):
    pano.get_vsys_data()

@st.cache_resource
def create_pano():
    pano = PanoramaAPI()
    pano.login()
    return pano

df = pd.read_json('demo_data.json')
# df.index = df['data_center_name']
df.rename(columns={'data_center_name': 'Data Center'}, inplace=True)
pano = create_pano

# Create a dropdown menu in the sidebar with the data centers as options
selected_data_center = st.sidebar.selectbox('Select a Data Center', df['Data Center'].unique())

# Filter the DataFrame based on the selected data center
filtered_df = df[df['Data Center'] == selected_data_center]
# Pull the keys out of the zones column, casting it to a list to eliminate PD series object
zones = list(filtered_df['zones'])[0]
# st.dataframe(data = zones, hide_index=True)
selected_zone = st.sidebar.selectbox(f'Select a Zone Within {selected_data_center}', zones)
print(type(zones[selected_zone]))
current_zone = pd.DataFrame(zones[selected_zone])

# Make selectable rows of firewalss in selected zone
fw_event = st.dataframe(data=current_zone,use_container_width=True, on_select="rerun", hide_index=True, selection_mode="multi-row")
# st.dataframe(data = filtered_df['zones'][0][selected_zone], hide_index=True)

#Create new dataframe with selected firewalls
st.header('Reserve VSYS on selected Firewalls')
fw_selection = fw_event.selection.rows
filtered_df = current_zone.iloc[fw_selection]
if not filtered_df.empty:
    if st.button('Submit'):
        st.session_state['selected_firewalls'] = filtered_df['firewall_name'].tolist()
        st.rerun()
# st.dataframe(data = filtered_df, hide_index=True)  #TODO add column_config=column_configuration move to new page
