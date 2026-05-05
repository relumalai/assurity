
import requests
from requests.exceptions import HTTPError, ConnectionError, JSONDecodeError, RequestException


class NativeValidator:
    """
    Validates API response fields using plain Python dict access.
    Expects self.response_json to be set by the host class (ValidateAPI).
    """

    def _result(self, check, expected, actual):

        # return the result keys 
        return {
            "check": check,
            "expected": expected,
            "actual": actual,
            "Result": "Pass" if actual == expected else "Fail",
        }

    def validate_name(self, expected_name: str):
        try:
            actual = self.response_json["Name"]
        except KeyError:
            return self._result("Native – Validate Name", expected_name, "field missing from response")
        return self._result("Native – Validate Name", expected_name, actual)

#compare as bool sing its bool in response
    def validate_relist(self, expected_relist_state: bool):
        try:
            actual = self.response_json["CanRelist"]
        except KeyError:
            return self._result("Native – Validate CanRelist", expected_relist_state, "field missing from response")
        return self._result("Native – Validate CanRelist", expected_relist_state, actual)

    def validate_promotion(self, promotion_name: str, expected_promotion_gallery_description: str):
        try:
            promotions = self.response_json["Promotions"]
            actual = next(
                (p["Description"] for p in promotions if p["Name"] == promotion_name),
                None,
            )
        except KeyError:
            return self._result(
                f"Native – Validate Promotion: {promotion_name}",
                expected_promotion_gallery_description,
                "field missing from response",
            )
        return self._result(
            f"Native – Validate Promotion: {promotion_name}",
            expected_promotion_gallery_description,
            actual,
        )