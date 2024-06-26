import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

"""
# Rackspace Demo Dashboard
## Palo Alto 1410 Utilization

Click on the Data Center at the left to show the available PA1410's
"""

df = pd.read_json('demo_data.json')
# df.index = df['data_center_name']
df.rename(columns={'data_center_name': 'Data Center'}, inplace=True)

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


st.dataframe(data=current_zone, hide_index=True)
# st.dataframe(data = filtered_df['zones'][0][selected_zone], hide_index=True)
