"""
validateapi_core.py — orchestration layer

Strategy:
  Three mixin classes each implement the same three validate_* method names using
  a different technique (native dict access, JMESPath, Pydantic). ValidateAPI inherits
  from all three and call them explicitly, making the union explicit, unambiguous, and readable.
"""

import os
import requests

from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError, JSONDecodeError, RequestException
from tabulate import tabulate

from JmespathValidator import JMESPathValidators
from nativevalidation import NativeValidator
from PydanticValidator import PydanticValidators


load_dotenv()


class ErrInFetchingAPI(Exception):
    pass


class ValidateAPI(NativeValidator, JMESPathValidators, PydanticValidators):
    """
    Main orchestration class.

    Inherits validate three  classes validate_* method
    calls all three parent implementations explicitly one per technique — for side-by-side comparison.

    """

    def __init__(self):
        # FIX: was missing load_dotenv(); env vars from .env were never loaded
        base_url = os.getenv("BASE_URL")
        catalogue = os.getenv("CATALOGUE")
        category_id = os.getenv("CATEGORY_ID")

        if not all([base_url, category_id, catalogue]):
            raise EnvironmentError("Configuration Error, check env file is setup properly.")

        
        self.url = f"{base_url}/Categories/{category_id}/Details.json?catalogue={catalogue}"
        self.response_json = self._fetch_response()
        if "ErrorDescription" in self.response_json:
            raise ErrInFetchingAPI("There seems to be error, with the request, unable to proceed.") 
     
#method to make the api get call, validate the response and return it.
    def _fetch_response(self) -> dict:
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


    # --- call every parent explicitly so all three techniques are exercised ---

    def validate_name(self, expected_name: str):
        return [
            NativeValidator.validate_name(self, expected_name),
            JMESPathValidators.validate_name(self, expected_name),
            PydanticValidators.validate_name(self, expected_name),
        ]

    def validate_relist(self, expected_relist_state: bool):
        return [
            NativeValidator.validate_relist(self, expected_relist_state),
            JMESPathValidators.validate_relist(self, expected_relist_state),
            PydanticValidators.validate_relist(self, expected_relist_state),
        ]

    def validate_promotion(self, promotion_name: str, expected_promotion_gallery_description: str):
        return [
            NativeValidator.validate_promotion(self, promotion_name, expected_promotion_gallery_description),
            JMESPathValidators.validate_promotion(self, promotion_name, expected_promotion_gallery_description),
            PydanticValidators.validate_promotion(self, promotion_name, expected_promotion_gallery_description),
        ]
