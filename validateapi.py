# Import needed packages

import os
import requests
import jmespath
import pydantic
import json

from tabulate import tabulate
from requests.exceptions import HTTPError, ConnectionError, JSONDecodeError, RequestException
from dotenv import load_dotenv

#Custom Generic API Error class
class ErrInFetchingAPI(Exception):
    pass

#Main class for the solution
class ValidateAPI:

    # read the url, path and query parameter from a config file,
    # can be extended to run in different path, query parameter or different url point to different env

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

    '''
    uses generate to iterate over the dict. Down side is stops at the first match.
    '''

    def validate_promotion(self, promotion_name, expected_promotion_gallery_description):
        try:
            description = next((value["Description"] for value in self.responsedata["Promotions"] if value["Name"] == promotion_name), None)
        except KeyError:                # ✅ same level as try
            return self._results("Validate Promotion-Gallery's Description", "Field missing from response", expected_promotion_gallery_description)
        return self._results("Validate Promotion-Gallery's Description", description, expected_promotion_gallery_description)

    '''
    If Promtion named Gallery has multiple instance get all matches, print waring that there are more than 1 matches
    and validate if there is expected result among matches. Pydantic would solve this by adding file validator for a model, but same logic

    '''
    def validate_promotion_withduplicates(self, promotion_name, expected_promotion_gallery_description,testdata):

        descriptions = [value["Description"] for value in testdata["Promotions"] if value["Name"] == promotion_name]
        if not descriptions:
            return self._results("Validate Promotion-Gallery's Description","Field missing from response",expected_promotion_gallery_description)

        #check if there are more than one Description for Promotion.Name=Gallery
        if len(descriptions) > 1:
            all_descriptions = ", ".join(descriptions)
            #check if expected value is in the list, if a match is found with in duplicate, warn, and set the test to Fail.
            if expected_promotion_gallery_description in all_descriptions:
                return self._results("Validate Promotion-Gallery's Description - WARNING-DUPLICATES",f'One match found- [{all_descriptions}]',expected_promotion_gallery_description)
            else:
                return self._results("Validate Promotion-Gallery's Description - WARNING-DUPLICATES",f'No match found - [{all_descriptions}]',expected_promotion_gallery_description)
        return self._results("Validate Promotion-Gallery's Description",descriptions[0],expected_promotion_gallery_description)


#--------------- simple way to run the code-------------------
#can be extend to a commadline tool, calls all test by default

if __name__ == '__main__':

    #mock data for an edge case in one the validations

    mock1_responsedata = {
        "CategoryId": 6327,
        "Name": "Carbon credits",
        "CanRelist": True,
        "Promotions": [
            {"Id": 1, "Name": "Basic", "Description": "Lowest position in category", "Price": 0.0},
            {"Id": 2, "Name": "Gallery", "Description": "Good position"},
            {"Id": 3, "Name": "Feature", "Description": "Better position in category", "Price": 10.0},
            {"Id": 4, "Name": "Gallery", "Description": "Good position in category"},
        ]
    }

    mock2_responsedata = {
        "CategoryId": 6327,
        "Name": "Carbon credits",
        "CanRelist": True,
        "Promotions": [
            {"Id": 1, "Name": "Basic", "Description": "Lowest position in category", "Price": 0.0},
            {"Id": 2, "Name": "Gallery", "Description": "Good position"},
            {"Id": 3, "Name": "Feature", "Description": "Better position in category", "Price": 10.0},
            {"Id": 4, "Name": "Gallery", "Description": "Good "},
        ]
    }

    mock3_responsedata = {
        "CategoryId": 6327,
        "Name": "Carbon credits",
        "CanRelist": True,
        "Promotions": [
            {"Id": 1, "Name": "Basic", "Description": "Lowest position in category", "Price": 0.0},
            {"Id": 2, "Name": "Gallery", "Description": "Good position in category"},
            {"Id": 3, "Name": "Feature", "Description": "Better position in category", "Price": 10.0},
        ]
    }

    try:
        testapi = ValidateAPI()
        result=[
                testapi.validate_name(expected_name="Carbon credit"),
                testapi.validate_name(expected_name="Carbon credits"),
                testapi.validate_relist(expected_relist_state=True),
                testapi.validate_relist(expected_relist_state=False),
                testapi.validate_promotion(promotion_name="Gallery",expected_promotion_gallery_description="Good position in category"),
                testapi.validate_promotion(promotion_name="Gallery",expected_promotion_gallery_description="Low position in category"),
                testapi.validate_promotion_withduplicates(promotion_name="Gallery",expected_promotion_gallery_description="Good position in category",testdata=mock1_responsedata),
                testapi.validate_promotion_withduplicates(promotion_name="Gallery",expected_promotion_gallery_description="Good position in category",testdata=mock2_responsedata),
                testapi.validate_promotion_withduplicates(promotion_name="Gallery",expected_promotion_gallery_description="Good position in category",testdata=mock3_responsedata),
                ]
        print(tabulate(result, headers="keys", tablefmt="grid"))
    except ErrInFetchingAPI as err:
        print(f'Validation cannot be run due to error {err}')
