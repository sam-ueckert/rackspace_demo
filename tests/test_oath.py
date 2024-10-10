import requests
# import streamlit as st
from msal import ConfidentialClientApplication
from dotenv import load_dotenv
import os
load_dotenv("./.env")


def initialize_app():
    client_id = os.environ['AZURECLIENTID']
    tenant_id = os.environ['AZURETENTANTID']
    client_secret = os.environ['AZURESECRET']
    authority_url = f"https://login.microsoftonline.com/{tenant_id}"
    return ConfidentialClientApplication(client_id, authority=authority_url, client_credential=client_secret)


result = initialize_app()
print(result)