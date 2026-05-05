import jmespath

class JMESPathValidators:
    """
    Implements validation methods using JMESPath.
    Assumes self.response_json exists.
    """

    def _result(self, check_name, expected, actual, passed):
        return {
            "check": check_name,
            "expected": expected,
            "actual": actual,
            "passed": passed
        }

    def validate_name(self, expected_name: str):
        actual = jmespath.search("Name", self.response_json)
        passed = actual == expected_name

        return self._result(
            "Validate Name",
            expected_name,
            actual,
            passed
        )

    def validate_relist(self, expected_relist_state: bool):
        actual = jmespath.search("Relist", self.response_json)
        passed = actual == expected_relist_state

        return self._result(
            "Validate Relist",
            expected_relist_state,
            actual,
            passed
        )

    def validate_promotion(self, promotion_name: str, expected_promotion_gallery_description: str):
        promotions = jmespath.search("Promotions", self.response_json) or []

        promotion = next(
            (p for p in promotions if p.get("Name") == promotion_name),
            None
        )

        actual = promotion.get("Description") if promotion else None
        passed = actual == expected_promotion_gallery_description

        return self._result(
            f"Validate Promotion: {promotion_name}",
            expected_promotion_gallery_description,
            actual,
            passed
        )
