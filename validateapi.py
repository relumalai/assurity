# Import needed packages

import os
import requests
import jmespath
import pydantic

from tabulate import tabulate
from requests.exceptions import HTTPError, ConnectionError, JSONDecodeError, RequestException
from dotenv import load_dotenv

#Custom Generic API Error class
class ErrInFetchingAPI(Exception):
    pass

#Main class for the solution
class ValidateAPI:

# read the url, path and query parameter from a config file,
#can be extended to run in different path, query parameter or different url point to different env
 
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

#fetches the reposnse for the api and handle usual error

    def fetch_response(self):
        try:
            apiresponse = requests.get(self.url)
            apiresponse.raise_for_status()
            return apiresponse.json()
        except HTTPError as http_err:
            print(f'http error: {http_err} occured')
        except ConnectionError as con_err:
            print(f'Unable to connect to endpoint: {con_err}')
        except JSONDecodeError as jsonres_err:
            print(f'JSON response is invalid: {jsonres_err}')
        except RequestException as err:
            print(f'Unexpected Error: {err}')

# helper method to collate the results, make it easier read and format the results. 
    
    def _results(self,test,actual,expected):
        return {
                "Test" : test,
                "Actual" : actual,
                "Expected" : expected,
                "Result": "Pass" if actual == expected else "Fail"
                }
    
#---------------- validation metods--------------------#
#read the value, returns erron case key is not found and fails the va;idation
#allows to continue with other validation

    def validate_name(self,expected_name):
        try:
            value_in_response = self.responsedata["Name"]
        except KeyError:
            return self._results("Validate Name","Field missing form response",expected_name)
        return self._results("Validate Name",value_in_response,expected_name)


    def validate_relist(self, expected_relist_state: bool):
        try:
            state_of_relist = self.responsedata["CanRelist"]
        except KeyError:
            return self._results("Validate CanReList State","Field missing from response",True)
        return self._results("Validate CanReList State",state_of_relist,expected_relist_state)
        

    def validate_promotion(self, promotion_name, expected_promotion_gallery_description):
        try:
            description = next((value["Description"] for value in self.responsedata["Promotions"] if value["Name"] == promotion_name), None)
        except KeyError:
            return self._results("Validate Promotion-Gallery's Description","Filed missing from response",expected_promotion_gallery_description)
        return self._results("Validate Promotion-Gallery's Description",description,expected_promotion_gallery_description)

#--------------- simple way to run the code-------------------
#can be extend to a commadline tool, calls all test by default

if __name__ == '__main__':
    try:
        testapi = ValidateAPI()
        result=[
                testapi.validate_name(expected_name="Carbon credit"),
                testapi.validate_name(expected_name="Carbon credits"),
                testapi.validate_relist(expected_relist_state=True),
                testapi.validate_relist(expected_relist_state=False),
                testapi.validate_promotion(promotion_name="Gallery",expected_promotion_gallery_description="Good position in category"),
                testapi.validate_promotion(promotion_name="Gallery",expected_promotion_gallery_description="Low position in category"),
                ]
        print(tabulate(result, headers="keys", tablefmt="grid"))
    except ErrInFetchingAPI as err:
        print(f'Validation cannot be run due to error {err}')
