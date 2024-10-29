import requests
import toml
import os
from dotenv import load_dotenv

load_dotenv("./.env")
settings = toml.load("settings.toml")

TOKEN_URL = settings['FACTS_TOKEN_URL']
FACTS_URL = settings['FACTS_URL']
PER_PAGE = settings['PER_PAGE']
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


def get_facts(token, url):
    '''Get first page of facts from the API'''
    headers = {
        "X-Auth-Token": token
    }
    endpoint = url + f"?page_no=1&per_page={PER_PAGE}"
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def page_facts(token, url, firstpage):
    '''Get all pages of facts from the API'''
    current_page = firstpage['page_no']+1
    total_pages = firstpage['total_pages']
    device_list = list(firstpage['Data'])
    while current_page < total_pages:
        facts = get_facts(token, url + f"?page={current_page}")
        current_page += 1
        device_list.append(facts['Data'])

token = get_token(USERNAME, PASSWORD, "Rackspace", TOKEN_URL)['id']
