import datetime
import os
import re
import pytest
from unittest.mock import MagicMock
from requests import Response

from estela_requests.utils import (decode_job, elapsed_seconds_time,
                                   get_estela_response, parse_time)
from estela_requests.estela_http import EstelaHttpRequest



class TestEstelaRequestsUtils:
# Tests that the function returns 0 when start_time and end_time are the same
    def test_elapsed_seconds_time(self):
        start_time = '01/01/2022 00:00:00.000000'
        same_end_time = '01/01/2022 00:00:00.000000'
        diff_end_time = '01/01/2022 00:00:02.000000'
        assert elapsed_seconds_time(same_end_time, start_time) == 0.0
        assert elapsed_seconds_time(diff_end_time, start_time) == 2.0

        # Tests that the function correctly parses a valid datetime object
    def test_valid_datetime_object(self):
        assert parse_time(datetime.datetime(2022, 1, 1, 12, 0, 0, 0)) == '01/01/2022 12:00:00.000'

    def test_empty_datetime_object(self):
        time_pattern = r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}\.\d{3}"
        assert re.match(time_pattern, parse_time())
    
    # Tests that a valid JSON string is returned when JOB_INFO environment variable starts with '{'.
    def test_valid_json_in_decode_job(self):
        os.environ['JOB_INFO'] = '{"key": "value", "key2": "value2"}'
        assert decode_job() == {'key': 'value', 'key2': "value2"}
    
    def test_valid_job_info(self):
        os.environ["JOB_INFO"] = '''{
            "key":"jid.sid.pid",
            "spider":"sid",
            "auth_token":"your_auth_token",
            "api_host":"http://api_host.com",
            "args":{"arg1":"value1","arg2":"value2"},
            "collection": "b1709e50-6717-4913-af4c-49b72a8243f5",
            "unique":"True"}'''
        job_info = decode_job()
        assert job_info["spider"] == "sid"

        # Tests that a valid response object returns an EstelaResponse object
    def test_valid_response(self):
        req_obj = MagicMock(spec=EstelaHttpRequest)
        req_obj.method = "GET"
        response = MagicMock(spec=Response)
        response.url = 'http://example.com'
        response.content = b'example content'
        response.text = 'example content'
        response.status_code = 200
        response.request = req_obj
        response.elapsed = 1.0
        estela_response = get_estela_response(response)
        assert estela_response.url == 'http://example.com'
        assert estela_response.body == b'example content'
        assert estela_response.text == 'example content'
        assert estela_response.status_code == 200
        assert estela_response.request.method == 'GET'
