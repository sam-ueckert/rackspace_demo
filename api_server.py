from flask import Flask, request, jsonify
from paloaltosdk import PanoramaAPI
from dotenv import load_dotenv
from rackspace_functions import create_batch_vsys_reservations
import pandas as pd
import toml
from pathlib import Path
import os
from log_tools import setup_logger

load_dotenv("./.env")
settings = toml.load("settings.toml")
log_dir = settings['LOG_DIR']
log_file = settings['LOG_FILE']
log_path = Path(log_dir) / log_file
logger = setup_logger(log_path)


def create_local_pano():
    pano = PanoramaAPI()
    pano.IP = settings['PANORAMA']
    pano.Username = os.environ['SSO_UNAME']
    pano.Password = os.environ['SSO_PASS']
    return pano


app = Flask(__name__)


@app.route('/')
def api_splash():
    return 'This is the API server for the Panorama VSYS reservation system.'


@app.route('/create_vsys', methods=['POST'])
def create_vsys():
    device = request.form.get('device')
    vsys_name = request.form.get('vsys_name')

    if not device or not vsys_name:
        return 'Missing device or vsys_name', 400

    try:
        pano.login()
        resp = pano.create_vsys(vsys_name, 'auto', device)

    except Exception as e:
        return f"An error occurred: {e}", 500

    return resp


@app.route('/create_batch_reservation', methods=['POST'])
def create_batch_reservation():
    ''' Creates a batch of VSYS reservations on the Panorama.
        Requires a pandas DataFrame. Each for is an Index column,
        and a dictionary containing the device serial and the vsys device number.
        Seee rackspace_functions.create_batch_vsys_reservations for more details.'''
    try:
        # Parse the JSON payload
        data = request.get_json()
        df = pd.DataFrame(data)

        # Process the DataFrame
        resp = create_batch_vsys_reservations(df)

    except Exception as e:
        return f"An error occurred: {e}", 500

    return jsonify(resp)


# resp = pano.delete_vsys(serial="026701009940", vsys_id=3, )

if __name__ == '__main__':
    pano = create_local_pano()
    app.run()
