import json
from pprint import pprint

import requests


class ApiHelper:
    @classmethod
    def logger(cls, log_text_json):
        # pp = pprint.PrettyPrinter(indent=levels)
        # pp.pprint(log_text_json)
        pprint(log_text_json)

    @classmethod
    def request(cls, url_method: str, url: str, headers: str, payload: str, expected_status_code: int,
                expected_response_text: bool = None, the_files: bool = None):
        url = "https://www.dnd5eapi.co/api/" + url
        assert url_method in ({"POST", "GET", "DELETE", "PUT", "PATCH"}), "Needs to be a valid RestAPI Method"
        cls.logger("##### Python calls made to API #####")
        cls.logger("Begin")
        cls.logger("payload = " + str(payload))
        cls.logger("payload = json.dumps(payload)")
        cls.logger("headers=" + str(headers))
        payload = json.dumps(payload)
        cls.logger(
            "response = requests.request('" + url_method + "', '" + url + "', headers=headers, data=payload, verify=False)")
        cls.logger("Ends")
        if the_files is None:
            response = requests.request(url_method, url, headers=headers, data=payload, verify=False)
        else:
            response = requests.request("POST", url, headers=headers, files=the_files, verify=False)

        assert response.status_code == expected_status_code, "Expected Status code - " + str(expected_status_code) \
                                                             + " Got - " + str(response.status_code) + "\n" + \
                                                             response.text
        if expected_response_text is not None:
            assert response.text == expected_response_text

        if response.status_code in [413, 404, 405]:
            return response

        response_json = response.json()

        cls.logger("##### Response Output from API - Beginning #####")
        cls.logger(response_json)
        cls.logger("##### Response Output from API - End #####")
        cls.logger("")

        return response
