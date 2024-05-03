from pprint import pprint

from APIHelper import ApiHelper


def get_spells(spell=""):
    response = ApiHelper.request("GET", payload="",
                                 headers="", url="spells/" + spell,
                                 expected_status_code=200)
    return ApiHelper.return_json(response)


def get_lineage(index=""):
    response = ApiHelper.request("GET", payload="",
                                 headers="", url="races/" + index,
                                 expected_status_code=200)
    return ApiHelper.return_json(response)


def get_class(class_name=""):
    response = ApiHelper.request("GET", payload="",
                                 headers="", url="classes/" + class_name,
                                 expected_status_code=200)
    return ApiHelper.return_json(response)
