import streamlit_app as sa
import json
import toml
import streamlit as st
from paloaltosdk import PanoramaAPI
from dotenv import load_dotenv
# import time
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
logger = sa.logger
# Local funcions to cache data, using decorator


@log_exceptions(logger=logger)
@st.cache_data
def mock_device_data(_pano: PanoramaAPI):
    with open('json/devices.json', 'r') as f:
        local_device_data = json.load(f)
    return local_device_data


@st.cache_data
def mock_vsys_data(_pano: PanoramaAPI, devices):
    with open('json/vsys_data.json', 'r') as f:
        local_vsys_data = json.load(f)
    return local_vsys_data


sa.local_device_data = mock_device_data
sa.local_vsys_data = mock_vsys_data

sa.main()
