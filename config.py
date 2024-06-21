import logging
import logging
import urllib.parse as urlparse
import requests
from sqlalchemy import func
from dotenv import load_dotenv, set_key, get_key, find_dotenv

load_dotenv()
dotenv_path = find_dotenv()

def main():
    # Access key vault
    bh_client_id = get_key(dotenv_path, 'BH_CLIENT_ID')
    bh_username = get_key(dotenv_path, 'BH_USERNAME')
    bh_password = get_key(dotenv_path, 'BH_PASSWORD')
    bh_client_secret = get_key(dotenv_path, 'BH_CLIENT_SECRET')

    logging.info("Starting BH Rest Token Authentication")

    try:
        # BH OAuth 2.0 Authentication Flow
        # Get Auth Token
        bh_base_url = "https://auth-west.bullhornstaffing.com"
        bh_auth_url = f"{bh_base_url}/oauth/authorize?client_id={bh_client_id}&response_type=code&action=Login&username={bh_username}&password={bh_password}"
        auth_token_response = requests.get(bh_auth_url)
        auth_token = urlparse.parse_qs(urlparse.urlparse(auth_token_response.url).query)["code"][0]

        # Get Access Token
        bh_access_token_url = f"{bh_base_url}/oauth/token?grant_type=authorization_code&code={auth_token}&client_id={bh_client_id}&client_secret={bh_client_secret}"
        bh_access_token_response = requests.post(bh_access_token_url)
        access_token = bh_access_token_response.json()["access_token"]

        # Get REST login token
        rest_login_url = f"https://rest.bullhornstaffing.com/rest-services/login?version=*&access_token={access_token}"
        login_response = requests.get(rest_login_url)
        rest_token = login_response.json()["BhRestToken"]
        rest_url = login_response.json()["restUrl"]

        set_key(dotenv_path, 'BH_REST_TOKEN', rest_token)
        set_key(dotenv_path, 'BH_REST_URL', rest_url)

        return func.HttpResponse("OK")

    except Exception as ex:
        msg = ex.message
        if not msg:
            msg = str(ex)
        logging.exception(f"Failed to refresh token:{msg}")
        return func.HttpResponse(f"{msg}", status_code=500)

if __name__ == "__main__":
    main()