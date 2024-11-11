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
settings = toml.load("settings.toml")
log_dir = settings['LOG_DIR']
log_file = settings['LOG_FILE']
log_path = Path(log_dir) / log_file
logger = setup_logger(log_path)
# logger.info('Loadin Vsys Dashboard')
# print('Running scheduled tasks')


