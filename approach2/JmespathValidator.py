import jmespath


class JMESPathValidators:
    """
    Validates API response fields using JMESPath expressions.
    Expects self.response_json to be set by the host class (ValidateAPI).
    JMESPath shines with deeply nested JSON; useful here for consistency and future-proofing.
    """

    def _result(self, check, expected, actual):
        return {
            "check": check,
            "expected": expected,
            "actual": actual,
            "Result": "Pass" if actual == expected else "Fail",
        }

    def validate_name(self, expected_name: str):
        actual = jmespath.search("Name", self.response_json)
        return self._result("JMESPath – Validate Name", expected_name, actual)

#compare as bool sing its bool in response
    def validate_relist(self, expected_relist_state: bool):
        # FIX: was searching "Relist" — the API field is "CanRelist" (matches models.py and NativeValidator)
        actual = jmespath.search("CanRelist", self.response_json)
        return self._result("JMESPath – Validate CanRelist", expected_relist_state, actual)

    def validate_promotion(self, promotion_name: str, expected_promotion_gallery_description: str):
        promotions = jmespath.search("Promotions", self.response_json) or []
        promotion = next((p for p in promotions if p.get("Name") == promotion_name), None)
        actual = promotion.get("Description") if promotion else None
        return self._result(
            f"JMESPath – Validate Promotion: {promotion_name}",
            expected_promotion_gallery_description,
            actual,
        )
