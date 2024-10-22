import requests
import toml
import os
from dotenv import load_dotenv

load_dotenv("./.env")
settings = toml.load("settings.toml")

TOKEN_URL = settings['FACTS_TOKEN_URL']
USERNAME = settings['PANORAMA']
PASSWORD = os.environ['SSO_PW']


def get_token(username, password, domain_name, tokrn_url):
    url = "https://identity-internal.api.rackspacecloud.com/v2.0/tokens"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "auth": {
            "RAX-AUTH:domain": {
                "name": "Rackspace"
            },
            "passwordCredentials": {
                "username": "sam7330",
                "password": "New Fleet.4.feet"
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

