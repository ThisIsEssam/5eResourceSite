from pprint import pprint

from APIHelper import ApiHelper


def test_get_all_spells():
    response = ApiHelper.request("GET",payload={}, headers={}, url="spells/", expected_status_code=200)
    response_json = response.json()
    pprint(response_json)