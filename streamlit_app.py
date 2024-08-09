import pandas as pd
import streamlit as st
from paloaltosdk import PanoramaAPI
from dotenv import load_dotenv
import rackspace_functions as rf
# import time
import toml
import os
from pathlib import Path
# from pprint import pprint
from log_tools import setup_logger, log_exceptions


load_dotenv("./.env")
st.set_page_config(layout="wide")
settings = toml.load("settings.toml")
log_dir = settings['LOG_DIR']
log_file = settings['LOG_FILE']
log_path = Path(log_dir) / log_file
logger = setup_logger(log_path)
# logger.info('Loadin Vsys Dashboard')

"""
# Rackspace Vsys Dashboard
## Track allocated vsys by firewall

Click on the Data Center at the left to start
"""
@log_exceptions()
@st.cache_resource
def create_local_pano():
    pano = PanoramaAPI()
    pano.IP = os.environ['PANORAMA']
    pano.Username = os.environ['CDWU']
    pano.Password = os.environ['CDWP']
    pano.login()
    return pano


# create a cached PanoramaAPI object
pano = create_local_pano()

# Local funcions to cache data, using decorator
@log_exceptions(logger=logger)
@st.cache_data
def local_device_data(_pano: PanoramaAPI):
    return pano.get_devices()


@st.cache_data
def local_vsys_data(_pano: PanoramaAPI, devices):
    return pano.get_vsys_data(devices=devices)


@log_exceptions(logger=logger)
def get_local_data(pano: PanoramaAPI):
    '''Retrieves all devices and vysys data from Panorama'''
    all_devices = local_device_data(pano)
    all_vsys = local_vsys_data(pano, all_devices)
    return all_devices, all_vsys


@log_exceptions(logger=logger)
def load_sidebar_data():
    '''Loads the sidebar data from a json file (later API call)'''
    df = pd.read_json('demo_data.json')
    df.rename(columns={'data_center_name': 'Data Center'}, inplace=True)
    # Create a dropdown menu in the sidebar with the data centers as options
    selected_data_center = st.sidebar.selectbox('Select a Data Center',
                                                df['Data Center'].unique())
    # Filter the DataFrame based on the selected data center
    filtered_df = df[df['Data Center'] == selected_data_center]
    '''
    Pull the keys out of the zones column,
    casting it to a list to eliminate PD series object'''
    zones = list(filtered_df['zones'])[0]
    # st.dataframe(data = zones, hide_index=True)
    selected_zone = st.sidebar.selectbox(f'Select a Zone Within {selected_data_center}', zones)
    current_zone = pd.DataFrame(zones[selected_zone])


@log_exceptions(logger=logger)
def make_reservations(edit_fw_df, fw_event):
    if not edit_fw_df.empty:
        if not edit_fw_df.iloc[-1]['Synced']:
            fw_event.selection.rows.pop()
            # fw_selection.pop
            edit_fw_df = edit_fw_df.iloc[:-1]
            st.write(
                    ''''**<span style="font-size:24px;color:red;">Selected
                    firewall out of sync. Wait, clear cache, and refresh.</span>**''',
                    unsafe_allow_html=True)
            # st.rerun()
            
        edited_fw_df = st.data_editor(data=edit_fw_df,
                                      use_container_width=True,
                                      hide_index=True,
                                      disabled=['Firewall'],
                                      column_order=['Firewall', 'Vsys Device Number']
                                      )
        if st.button('Submit'):
            try:
                resp = rf.create_batch_vsys_reservations(reservations=edited_fw_df, devices=all_devices)
                st.write(resp)
                st.rerun()
            except Exception as e:
                logger.error(f'Error creating reservations: {e}')
                st.write(e)


@log_exceptions(logger=logger)
def create_tabs(vsys_df):
    view, reserve = st.tabs(['View Vsys Data', 'Create VSYS Reservation'])

    with view:
        # Apply custom CSS to set the width of the container
        st.markdown(
            """
            <style>
            .view-container {
                max-width: 2000px;  /* Adjust the width as needed */
                margin: auto;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        # column_config={
        #             "Vsys Display Names": st.column_config.Column(
        #                 None, width=1000),
        #             }
        st.header('View Vsys Details')
        logger.info('Viewing Vsys Details')
        try:
            vsys_display_df = vsys_df.rename(columns={'vsys_max': 'Max Vsys',
                                                      'vsys_used': 'Used Vsys',
                                                      'vsys_free': 'Free Vsys',
                                                      'hostname': "Firewall",
                                                      'vsys_in_use': 'Vsys Display Names'},
                                             inplace=False)
        except Exception as e:
            logger.error(f'Error renaming columns: {e}')
            st.write(e)
        for index, row in vsys_display_df.iterrows():
            
            if not row['Synced']:
                vsys_display_df.at[index, 'Vsys Display Names'] = ['''Syncing peers.
                                                                     Please wait 5 min,
                                                                     clear cache
                                                                     and refresh.''']
                continue
            vsys_display_df.at[index, 'Vsys Display Names'] = [i['display-name'] for i in row['Vsys Display Names']]
        st.dataframe(data=vsys_display_df,
                     hide_index=True,
                     use_container_width=False,
                     width=None,
                     column_order=['Firewall', 'Vsys Display Names'])
    with reserve:
        st.header('Select Firewalls to Reserve VSYS')

        vsys_display_df = vsys_df.rename(columns={'vsys_max': 'Max Vsys',
                                                  'vsys_used': 'Used Vsys',
                                                  'vsys_free': 'Free Vsys',
                                                  'hostname': "Firewall"},
                                         inplace=False)
        # Make selectable rows of firewalss in selected zone
        fw_event = st.dataframe(data=vsys_display_df, 
                                use_container_width=False,
                                on_select="rerun", 
                                hide_index=True, 
                                selection_mode="multi-row",
                                column_order=['Firewall',
                                              'Max Vsys',
                                              'Used Vsys',
                                              'Free Vsys']
                                )

       
        st.header('Reserve VSYS on selected Firewalls')
         # Create new dataframe with selected firewalls
        fw_selection = fw_event.selection.rows
        ''' add all selected rows to a new dataframe.
        Each click will rerun the script, so the dataframe
        will be updated with the new selection'''
        edit_fw_df = vsys_display_df.iloc[fw_selection]
        # add a column to the new dataframe to allow the user to input a reserved vsys id
        edit_fw_df['Vsys Device Number'] = None

        # Working with the selected rows (firewalls)
        make_reservations(edit_fw_df, fw_event)


''' Get all device data, then pass this data to other functions 
instead of continuing to query Panorama'''
all_devices, all_vsys = get_local_data(pano)

## Mock sidebar data
load_sidebar_data()
## end mock sidebar data

# convert the vsys data to a dataframe
vsys_df = pd.DataFrame(all_vsys)
# Create tabbed view
create_tabs(vsys_df)


# st.dataframe(data = edit_fws, hide_index=True)  #TODO add column_config=column_configuration move to new page
