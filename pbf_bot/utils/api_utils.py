import requests
from requests.exceptions import RequestException
from .config import API_URL, ACCESS_ID
from datetime import datetime

requests.packages.urllib3.disable_warnings()


class Singleton(type):
    def __init__(cls, name, bases, mmbs):
        super(Singleton, cls).__init__(name, bases, mmbs)
        cls._instance = super(Singleton, cls).__call__()

    def __call__(cls, *args, **kw):
        return cls._instance


class Utils(metaclass=Singleton):

    def __init__(self):
        self._access_token = None
        self.start_datetime = None
        print(f"IMPORTANT: Initializing Utils with accessId: {ACCESS_ID}")
        self._access_token = self._get_token(ACCESS_ID)
        self.start_datetime = datetime.now()

        if self._access_token is not None:
            print("IMPORTANT: got access token")
        else:
            print("IMPORTANT: failed getting access token, try again later")

    def _get_token(self, access_id):
        token = None

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json-patch+json"}

        data = {
            "accessID": access_id
        }

        try:
            response = requests.post(API_URL + "/Authentication/GetAccessToken", json=data, headers=headers,
                                     verify=False)

            if response.status_code == 200:
                data = response.json()
                token = data["token"]
            else:
                print(response)

        except RequestException as rqe:
            print("IMPORTANT: Failed getting access token")
            print(rqe)
        except Exception as e:
            print("IMPORTANT: Failed getting access token")
            print(e)

        return token

    def update_token(self):
        self._access_token = self._get_token(ACCESS_ID)
        self.start_datetime = datetime.now()

        return self._access_token is not None

    def check_api_token_is_inspired(self):
        dt_now = datetime.now()
        dt_diff = (dt_now - self.start_datetime).total_seconds()
        return dt_diff >= 86000

    def check_code(self, series, number):
        if self.check_api_token_is_inspired():
            self.update_token()

        if self._access_token is None:
            if not self.update_token():
                print("IMPORTANT: failed getting access token, try again later")

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + self._access_token,
            "Content-Type": "application/json-patch+json"}

        data = {
            "usid": "",
            "series": series,
            "number": number,
            "udid": "",
            "checkerData": {
                "prescriptionId": "string",
                "checkedOrgBin": "string",
                "checkedOrgName": "string",
                "checkedAddress": "string"
            },
            "location": [
                0
            ]
        }

        response = None

        try:
            response = requests.post(API_URL + "/Checker/CheckCode", json=data, headers=headers, verify=False)
            if response.status_code == 200:
                return response.json()
            if response.status_code == 401:
                print("IMPORTANT: Authorization Failed.")

        except RequestException as rqe:
            print("IMPORTANT: Failed getting check")
            print(rqe)
        except Exception as e:
            print("IMPORTANT: Failed getting access token")
            print(e)

        return response
