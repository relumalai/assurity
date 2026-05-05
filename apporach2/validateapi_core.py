# validateapi - core v2
# the idea is implement vaidation using navive python (as in approach1), use jmespath package and finally pydantic way.
# jmespath is good in case of nested json, (this response dos not have to many nested elemens)
# pydantic is more of a stric validtion with schema define as model. Useful in testing integration apis.
# Putting all to gether with inheritance and explicit calling of methods to make it clean with out ambiguity.

import os
import requests
from tabulate import tabulate
from requests.exceptions import HTTPError, ConnectionError, JSONDecodeError, RequestException
from validators.pydantic_validators import PydanticValidators


# Custom Generic API Error class
class ErrInFetchingAPI(Exception):
    pass


class ValidateAPI(NativeValidator,JemespathValidator,PydanticValidators):
    """
    Main orchestration class.
    Validation behavior comes from inheritance.
    """

    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.catalogue = os.getenv("CATALOGUE")
        self.category_id = os.getenv("CATEGORY_ID")

        if not self.base_url:
            raise ErrInFetchingAPI("BASE_URL not set")

        self.response_json = self._fetch_api_response()

    def _fetch_api_response(self):
        try:
            response = requests.get(
                f"{self.base_url}/{self.catalogue}/{self.category_id}"
            )
            response.raise_for_status()
            return response.json()

        except (HTTPError, ConnectionError, JSONDecodeError, RequestException) as err:
            raise ErrInFetchingAPI(err)
