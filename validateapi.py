# Import needed packages

import os
from dotenv import load_dotenv
import requests
from requests.exceptions import HTTPError, ConnectionError, JSONDecodeError, RequestException
import jmespath
import pydantic


class ErrInFetchingAPI(Exception):
    pass


class ValidateAPI:

    def __init__(self):
        #intial values
        load_dotenv()

        base_url = os.getenv('BASE_URL')
        categoryid = os.getenv('CATEGORY_ID')
        catalogue = os.getenv('CATALOGUE')
        
        if not all([base_url, categoryid, catalogue]):
            raise EnvironmentError("Configuration Error, check env file is setup properly.")
        
        self.url = f"{base_url}/Categories/{categoryid}/Details.json?catalogue={catalogue}"
        self.responsedata = self.fetch_response()
        if "ErrorDescription" in self.responsedata:
            raise ErrInFetchingAPI("There seems to be error, with the request, unable to proceed.") 


    def fetch_response(self):
        try:
            apiresponse = requests.get(self.url)
            apiresponse.raise_for_status()
            return apiresponse.json()
        except HTTPError as http_err:
             HTTPError(f'http error: {http_err} occured')
        except ConnectionError as con_err:
            print(f'Unable to connect to endpoint: {con_err}')
        except JSONDecodeError as jsonres_err:
            print(f'JSON response is invalid: {jsonres_err}')
        except RequestException as err:
            print(f'Unexpected Error: {err}')

    def validate_name(self):
        assert self.responsedata["Name"] == "Carbon credits"


    def validate_relist(self):
        assert self.responsedata["CanRelist"] is True

    def validate_promotion(self):
        description = next((value["Description"] for value in self.responsedata["Promotions"] if value["Name"] == "Gallery"), None)
        assert description == "Good position in category"



if __name__ == '__main__':
    testapi = ValidateAPI()
    testapi.validate_name()
    testapi.validate_relist()
    testapi.validate_promotion()




