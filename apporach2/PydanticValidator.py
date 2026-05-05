from validators.models import Listing
from pydantic import ValidationError


class PydanticValidators:
    """
    Validation implementation using Pydantic models.
    """

    def _parse(self):
        try:
            return Listing.model_validate(self.response_json)
        except ValidationError as e:
            raise ValueError(f"Pydantic validation failed: {e}")

    def _result(self, check_name, expected, actual, passed):
        return {
            "check": check_name,
            "expected": expected,
            "actual": actual,
            "passed": passed
        }

    def validate_name(self, expected_name: str):
        data = self._parse()
        actual = data.Name
        passed = actual == expected_name

        return self._result(
            "Validate Name",
            expected_name,
            actual,
            passed
        )

    def validate_relist(self, expected_relist_state: bool):
        data = self._parse()
        actual = data.Relist
        passed = actual == expected_relist_state

        return self._result(
            "Validate Relist",
            expected_relist_state,
            actual,
            passed
        )

    def validate_promotion(self, promotion_name: str, expected_promotion_gallery_description: str):
        data = self._parse()

        promotion = next(
            (p for p in data.Promotions if p.Name == promotion_name),
            None
        )

        actual = promotion.Description if promotion else None
        passed = actual == expected_promotion_gallery_description

        return self._result(
            f"Validate Promotion: {promotion_name}",
            expected_promotion_gallery_description,
            actual,
            passed
        )
