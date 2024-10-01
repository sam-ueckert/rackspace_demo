import requests
import streamlit as st
from msal import ConfidentialClientApplication
import toml
from dotenv import load_dotenv
import os
load_dotenv("./.env")

settings = toml.load("settings.toml")
AUTHORITY_URL = settings["AUTHORITY_URL"]


def initialize_app(client_id, tenant_id, client_secret):
    authority_url = f"{AUTHORITY_URL}{tenant_id}"
    return ConfidentialClientApplication(client_id,
                                         authority=authority_url,
                                         client_credential=client_secret)


def acquire_access_token(app, code, scopes, redirect_uri):
    return app.acquire_token_by_authorization_code(code, scopes=scopes, redirect_uri=redirect_uri)


def fetch_user_data(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    graph_api_endpoint = "https://graph.microsoft.com/v1.0/me"
    response = requests.get(graph_api_endpoint, headers=headers)
    return response.json()


def authentication_process(app):
    scopes = ["User.Read"]
    redirect_uri = settings["REDIRECT_URI"]
    auth_url = app.get_authorization_request_url(scopes, redirect_uri=redirect_uri)
    st.markdown(f"Please go to [this URL]({auth_url}) and authorize the app.")
    if st.query_params.get("code"):
        st.session_state["auth_code"] = st.query_params.get("code")
        token_result = acquire_access_token(app, st.session_state.auth_code, scopes, redirect_uri)
        if "access_token" in token_result:
            user_data = fetch_user_data(token_result["access_token"])
            return user_data
        else:
            st.error("Failed to acquire token. Please check your input and try again.")


def login_ui():
    st.title("Microsoft Authentication")
    app = initialize_app(client_id=os.environ["AZURE_CLIENT_ID"],
                         tenant_id=os.environ["AZURE_TENTANT_ID"],
                         client_secret=os.environ["AZURE_CLIENT_SECRET"])
    user_data = authentication_process(app)
    if user_data:
        st.write("Welcome, ", user_data.get("displayName"))
        st.session_state["authenticated"] = True
        st.session_state["display_name"] = user_data.get("displayName")
        st.rerun()
