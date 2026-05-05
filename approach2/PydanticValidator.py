
from functools import cached_property

from models import Listing
from pydantic import ValidationError


class PydanticValidators:
    """
    Basic Validation of API response fields via a Pydantic model. Partial generated one in absense of Schema, and assuming it
    making type errors explicit rather than silent.

    """

    @cached_property
    def _parsed(self) -> Listing:
        try:
            return Listing.model_validate(self.response_json)
        except ValidationError as e:
            raise ValueError(f"Pydantic validation failed: {e}")

    def _result(self, check, expected, actual):
        return {
            "check": check,
            "expected": expected,
            "actual": actual,
            "Result": "Pass" if actual == expected else "Fail",
        }

    def validate_name(self, expected_name: str):
        actual = self._parsed.Name
        return self._result("Pydantic – Validate Name", expected_name, actual)

#compare as bool sing its bool in response
    def validate_relist(self, expected_relist_state: bool):
        actual = self._parsed.CanRelist
        return self._result("Pydantic – Validate CanRelist", expected_relist_state, actual)

    def validate_promotion(self, promotion_name: str, expected_promotion_gallery_description: str):
        promotion = next(
            (p for p in self._parsed.Promotions if p.Name == promotion_name),
            None,
        )
        actual = promotion.Description if promotion else None
        return self._result(
            f"Pydantic – Validate Promotion: {promotion_name}",
            expected_promotion_gallery_description,
            actual,
        )
