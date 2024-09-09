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
db_path = Path(settings['DB_PATH'])
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
def get_local_data(pano: PanoramaAPI, dg_list: list):
    '''Retrieves all devices and vysys data from Panorama'''
    all_devices = local_device_data(pano)
    filtered_serials = rf.get_serials_from_dgs(pano, dg_list)
    in_scope_devices = rf.filter_devices_by_serial(all_devices, filtered_serials)
    if in_scope_devices:
        all_vsys = local_vsys_data(pano, in_scope_devices)
    else:
        all_vsys = local_vsys_data(pano, all_devices)
    return all_devices, all_vsys, in_scope_devices


@log_exceptions(logger=logger)
def combine_db_pano_data(db, all_vsys):
    '''Combines the data from the CMDB and the Panorama API'''
    # If HA serials are present, use lower serial as the key
    all_vsys['serial'] = all_vsys['serial'].astype(str)
    if 'lower_serial' and 'higher_serial' in all_vsys.columns:
        all_vsys['serial'] = all_vsys.apply(
            lambda row: row['lower_serial'] if pd.notnull(row['lower_serial']) else row['serial'], axis=1
        )

    merged_df = pd.merge(all_vsys, db, on='serial', how='left')
    merged_df['Available Vsys'] = merged_df['vsys_capacity'] - merged_df['vsys_used']
    return merged_df


@log_exceptions(logger=logger)
def load_db_data():
    '''Loads the data from a json file (later API call)'''
    df = pd.read_json(db_path, dtype={'serial': str})
    df.rename(columns={'datacenter': 'Data Center',
                       'aggr': 'Aggr Zone'}, inplace=True)

    return df


@log_exceptions(logger=logger)
def load_sidebar_data(df):
    '''Loads the sidebar data from a json file (later API call)'''

    # Create a dropdown menu in the sidebar with the data centers as options
    # add an All option at the top
    selected_data_center = st.sidebar.selectbox('Select a Data Center',
                                                ['All'] + list(df['Data Center'].unique()), index=0)
    # Filter the DataFrame based on the selected data center
    filtered_df = df[df['Data Center'] == selected_data_center]
    """
    Pull the keys out of the zones column,
    casting it to a list to eliminate PD series object"""
    zones = list(filtered_df['Aggr Zone'].unique())
    # add an All option at the top
    selected_zone = st.sidebar.selectbox(f'Select an Aggr Zone Within {selected_data_center}',
                                         ['All'] + zones, index=0)
    # current_zone = pd.DataFrame(zones[selected_zone])
    return selected_data_center, selected_zone


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
                resp = rf.create_batch_vsys_reservations(reservations=edited_fw_df,
                                                         devices=all_devices)
                st.write(resp)
                st.rerun()
            except Exception as e:
                logger.error(f'Error creating reservations: {e}')
                st.write(e)


@log_exceptions(logger=logger)
def rename_culumns(vsys_df):
    '''Rename columns for display purposes'''
    try:
        vsys_display_df = vsys_df.rename(columns={'vsys_max': 'Max Vsys',
                                                  'vsys_used': 'Used Vsys',
                                                  'vsys_free': 'Free Vsys',
                                                  'hostname': "Firewall",
                                                  'vsys_in_use': 'Vsys Display Names',
                                                  'higher_serial': 'Peer Serial',
                                                  'public_vlans': 'Public VLANs',
                                                  'vsys_capacity': 'Vsys Capacity',
                                                  'public_vlans': 'Public VLANs',
                                                  'serial': 'Serial'},
                                         inplace=False)
    except Exception as e:
        logger.error(f'Error renaming columns: {e}')
        st.write(e)
    return vsys_display_df


@log_exceptions(logger=logger)
def filter_tab_view(vsys_df, datacenter, zone):
    '''Filter the DataFrame based on the datacenter and zone'''
    # st.write(f'Datacenter: {datacenter}, Zone: {zone}')
    if datacenter and zone and datacenter != 'All' and zone != 'All':
        filtered_df = vsys_df[
            (vsys_df['Data Center'] == datacenter) &
            (vsys_df['Aggr Zone'] == zone)
        ]
    elif datacenter and datacenter != 'All':
        filtered_df = vsys_df[
           vsys_df['Data Center'] == datacenter
        ]
    elif zone and zone != 'All':
        filtered_df = vsys_df[
            vsys_df['Aggr Zone'] == zone
        ]
    else:
        filtered_df = vsys_df
    return filtered_df


@log_exceptions(logger=logger)
def create_zone_totals_df(vsys_df):
    '''Create a DataFrame with zone totals'''
    try:
        # Group by 'Aggr Zone' and calculate the totals
        zone_totals = vsys_df.groupby('Aggr Zone').agg({
            'Max Vsys': 'sum',
            'Used Vsys': 'sum',
            'Free Vsys': 'sum'
        }).reset_index()

        # Rename columns for display purposes
        zone_totals_df = zone_totals.rename(columns={
            'Aggr Zone': 'Aggr Zone',
            'Max Vsys': 'Total Max Vsys',
            'Used Vsys': 'Total Used Vsys',
            'Free Vsys': 'Total Free Vsys'
        })

        return zone_totals_df
    except Exception as e:
        logger.error(f'Error creating zone totals DataFrame: {e}')
        st.write(e)
        return pd.DataFrame()
    

@log_exceptions(logger=logger)
def create_tabs(vsys_df, datacenter=None, zone=None):
    view, reserve, zone_totals = st.tabs(['View Vsys Data', 'Create VSYS Reservation', 'Zone Totals'])
    vsys_display_df = rename_culumns(vsys_df)
    filtered_df = filter_tab_view(vsys_display_df, datacenter, zone)
    with view:
        # Apply custom CSS to set the width of the container
        st.markdown(
            """
            <style>
            .view-container {
                max-width: 500px;  /* Adjust the width as needed */
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

        for index, row in filtered_df.iterrows():
            if not row['Synced']:
                filtered_df.at[index, 'Vsys Display Names'] = ["Syncing peers. Please wait 5 min, "
                                                               "clear cache and refresh."]
                continue
            # pulls the vsys display names out of the list of dictionaries
            filtered_df.at[index, 'Vsys Display Names'] = [i['display-name']
                                                           for i in row['Vsys Display Names']]

        st.dataframe(data=filtered_df,
                     hide_index=True,
                     use_container_width=False,
                     width=1300,
                     column_order=['Firewall',
                                   'Vsys Display Names',
                                   'Vsys Capacity',
                                   'Used Vsys',
                                   'Available Vsys',
                                   'Public VLANs',
                                   'Serial',
                                   'Peer Serial'])
    with reserve:
        column_config = {
            "favorite": st.column_config.SelectboxColumn(
                "✔",
                help="✔",
                default=False,
            )
        } #  Future use: move to st.data_editor to acitvate this config
        st.header('Select Firewalls to Reserve VSYS')
        # Make selectable rows of firewalss in selected zone
        fw_event = st.dataframe(data=filtered_df,
                                column_config=column_config,
                                use_container_width=False,
                                on_select="rerun",
                                hide_index=True,
                                selection_mode="multi-row",
                                column_order=['Firewall',
                                              'Vsys Capacity',
                                              'Used Vsys',
                                              'Public VLANs',
                                              'Available Vsys',]
                                )

        st.header('Reserve VSYS on selected Firewalls')
        # Create new dataframe with selected firewalls
        fw_selection = fw_event.selection.rows
        ''' add all selected rows to a new dataframe.
        Each click will rerun the script, so the dataframe
        will be updated with the new selection'''
        edit_fw_df = filtered_df.iloc[fw_selection]
        # add a column to the new dataframe to allow the user to input a reserved vsys id
        edit_fw_df['Vsys Device Number'] = None

        # Working with the selected rows (firewalls)
        make_reservations(edit_fw_df, fw_event)
    with zone_totals:
        st.header('Zone Totals')
        zone_totals_df = create_zone_totals_df(filtered_df)
        st.dataframe(data=zone_totals_df, hide_index=True)


def main():
    ''' Get all device data, then pass this data to other functions
    instead of continuing to query Panorama'''
    global all_devices, all_vsys, in_scope_devices
    st.image("rackspace_logo.jpg", width=200)
    st.header(":blue[Vsys Dashboard]",)
    all_devices, all_vsys, in_scope_devices = get_local_data(pano, settings['DEVICE_GRPS'])
    db = load_db_data()
    merged_df = combine_db_pano_data(db, pd.DataFrame(all_vsys))
    datacenter, zone = load_sidebar_data(db)
    # st.write(type(db))
    # convert the vsys data to a dataframe
    vsys_df = pd.DataFrame(merged_df)
    # Create tabbed view
    create_tabs(vsys_df, datacenter=datacenter, zone=zone)


# st.dataframe(data = edit_fws, hide_index=True)
# #TODO add column_config=column_configuration move to new page
if __name__ == '__main__':
    main()
