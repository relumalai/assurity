#run test

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
