import requests
import toml
import os
from dotenv import load_dotenv

load_dotenv("./.env")
settings = toml.load("settings.toml")

TOKEN_URL = settings['FACTS_TOKEN_URL']
USERNAME = os.environ['SSO_UNAME']
PASSWORD = os.environ['SSO_PW']


def get_token(username, password, domain_name, token_url):
    # url = "https://identity-internal.api.rackspacecloud.com/v2.0/tokens"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "auth": {
            "RAX-AUTH:domain": {
                "name": domain_name
            },
            "passwordCredentials": {
                "username": username,
                "password": password
            }
        }
    }

    response = requests.post(token_url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

