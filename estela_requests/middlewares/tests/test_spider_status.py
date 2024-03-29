# Generated by CodiumAI
from datetime import timedelta
from unittest.mock import Mock, patch

# Dependencies:
# pip install pytest-mock
import pytest
import requests

from estela_requests.exceptions import InvalidJobFormatError
from estela_requests.middlewares.spider_status import SpiderStatusMiddleware

"""
Code Analysis

Main functionalities:
The SpiderStatusMiddleware class is responsible for updating the status of a spider job in Estela platform. It communicates with the Estela API to update the job status to RUNNING when the spider starts and to COMPLETED when the spider finishes. It also updates the job statistics, such as lifespan, item count, total bytes, and request count.

Methods:
- update_job: sends a PATCH request to the Estela API to update the job status and statistics.
- before_session: updates the job status to RUNNING before the spider session starts.
- after_session: updates the job status to COMPLETED after the spider session finishes and updates the job statistics.
- before_request and after_request: do not have any implementation.

Fields:
- api_host: the URL of the Estela API.
- auth_token: the authentication token to access the Estela API.
- job_url: the URL of the spider job in the Estela API.
- stats: a dictionary containing the spider job statistics, such as elapsed time, item count, total bytes, and request count.
"""
class TestSpiderStatusMiddleware:
    def test_update_job_valid_parameters(self):
        middleware = SpiderStatusMiddleware('1.2.3', 'http://localhost:8000', 'valid_token')

        with patch('requests.patch') as mock_patch:
            mock_patch.return_value = Mock(status_code=200)

            middleware.update_job('RUNNING', lifespan=timedelta(seconds=10), total_bytes=100, item_count=5, request_count=3)

            mock_patch.assert_called_once_with(
                'http://localhost:8000/api/projects/3/spiders/2/jobs/1',
                data={'status': 'RUNNING', 'lifespan': timedelta(seconds=10), 'total_response_bytes': 100, 'item_count': 5, 'request_count': 3},
                headers={'Authorization': 'Token valid_token'},
                timeout=20,
            )

    def test_update_job_valid_parameters_non_200_response(self, caplog):
        middleware = SpiderStatusMiddleware('1.2.3', 'http://localhost:8000', 'valid_token')
        with patch('requests.patch') as mock_patch:
            mock_patch.return_value = Mock(status_code=400)
            middleware.update_job('RUNNING', lifespan=timedelta(seconds=10), total_bytes=100, item_count=5, request_count=3)
            requests.patch.assert_called_once_with(
                'http://localhost:8000/api/projects/3/spiders/2/jobs/1',
                data={'status': 'RUNNING', 'lifespan': timedelta(seconds=10), 'total_response_bytes': 100, 'item_count': 5, 'request_count': 3},
                headers={'Authorization': 'Token valid_token'},
                timeout=20,
            )
            assert caplog.records[0].msg == "Failed to update job status, non-200 response"

    def test_update_job_request_exception(self):
        middleware = SpiderStatusMiddleware('1.1.1', 'http://localhost:8000', 'valid_token')
        with patch("requests.patch") as mock_patch:
            mock_patch.side_effect = requests.exceptions.RequestException
            with pytest.raises(requests.exceptions.RequestException):
                middleware.update_job('RUNNING', lifespan=timedelta(seconds=10), total_bytes=100, item_count=5, request_count=3)
                # requests.patch.assert_called_once_with(
                #     'http://localhost:8000/api/projects/1/spiders/1/jobs/1',
                #     data={'status': 'RUNNING', 'lifespan': timedelta(seconds=10), 'total_response_bytes': 100, 'item_count': 5, 'request_count': 3},
                #     headers={'Authorization': 'Token valid_token'},
                #     tiemout=20,
                # )

    # Tests that the job status is not updated with invalid lifespan parameter
    def test_update_job_invalid_lifespan_parameter(self):
        middleware = SpiderStatusMiddleware('1.1.1', 'http://localhost:8000', 'valid_token')
        with patch("requests.patch") as mock_patch:
            mock_patch.return_value = Mock(status_code=200)
            with pytest.raises(InvalidJobFormatError):
                middleware.update_job('RUNNING', lifespan='invalid_lifespan', total_bytes=100, item_count=5, request_count=3)
            requests.patch.assert_not_called()

    def test_after_session_calls_update_job_correctly(self):
        middleware = SpiderStatusMiddleware('1.1.1', 'http://localhost:8000', 'token')
        with patch.object(middleware, 'update_job') as update_job_mock:
            middleware.after_session()
            update_job_mock.assert_called_once_with('COMPLETED', lifespan=timedelta(seconds=0), item_count=0, total_bytes=0, request_count=0)

    def test_default_item_count(self):
        middleware = SpiderStatusMiddleware('jid.sid.pid', 'http://localhost:8000', 'token')
        with patch("requests.patch") as mock_patch:
            mock_patch.return_value = Mock(status_code=200)
            middleware.update_job('COMPLETED')
            requests.patch.assert_called_once_with(
                "http://localhost:8000/api/projects/pid/spiders/sid/jobs/jid",
                data={
                    'status': 'COMPLETED',
                    'lifespan': timedelta(seconds=0),
                    'total_response_bytes': 0,
                    'item_count': 0,
                    'request_count': 0
                },
                headers={'Authorization': 'Token token'},
                timeout=20,
            )

    # Tests that the job status is not updated when an invalid request_count parameter is provided
    def test_before_session_calls_update_job_correctly(self):
        middleware = SpiderStatusMiddleware('1.1.1', 'http://localhost:8000', 'token')
        with patch("requests.patch"), patch.object(middleware, "update_job") as update_job_mock:
            middleware.before_session()
            update_job_mock.assert_called_once_with('RUNNING')
            requests.patch.assert_not_called()
