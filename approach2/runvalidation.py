
from tabulate import tabulate
from validateapi_core import ErrInFetchingAPI, ValidateAPI


if __name__ == "__main__":
    try:
        api = ValidateAPI()

        # Each validate_* call now returns a list of 3 dicts (one per technique).
        # We flatten all result into a single list so tabulate renders one unified table.
        result = [
            api.validate_name(expected_name="Carbon credit"),
            api.validate_name(expected_name="Carbon credits"),
            api.validate_relist(expected_relist_state=True),
            api.validate_relist(expected_relist_state=False),
            api.validate_promotion(
                promotion_name="Gallery",
                expected_promotion_gallery_description="Good position in category",
            ),
            api.validate_promotion(
                promotion_name="Gallery",
                expected_promotion_gallery_description="Low position in category",
            ),
        ]
        print(result)
        # Flatten: each group is [native_result, jmespath_result, pydantic_result]
        rows = [row for group in result for row in group]

        print(tabulate(rows, headers="keys", tablefmt="grid"))

    except ErrInFetchingAPI as err:
        print(f"Validation cannot run — API fetch error: {err}")
