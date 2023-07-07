# Generated by CodiumAI
import pytest
import re
import requests
from unittest.mock import MagicMock, patch
from datetime import timedelta

from estela_requests.middlewares.spider_status import SpiderStatusMiddleware
from estela_requests.middlewares.requests_history import RequestsHistoryMiddleware
from estela_requests.middlewares.stats import StatsMiddleware
from estela_requests.middlewares.manager import MiddlewareManager
from estela_requests.estela_hub import EstelaHub
from estela_requests.estela_http import EstelaResponse, EstelaHttpRequest

"""
Code Analysis

Main functionalities:
The MiddlewareManager class is responsible for managing the middlewares used in the EstelaHub class. It allows for the creation of middleware instances from the EstelaHub instance and the application of before and after session middlewares.

Methods:
- __init__(self, middleware_list: List[EstelaMiddlewareInterface]) -> None: Initializes the MiddlewareManager instance with a list of middleware instances.
- from_estela_hub(cls, estela_hub: EstelaHub): Creates middleware instances from the EstelaHub instance and returns a MiddlewareManager instance.
- prioritize_middlewares(self) -> None: Method to prioritize middlewares. Currently, it does nothing.
- apply_before_session_middlewares(self, *args, **kwargs) -> None: Applies the before_session method of each middleware instance to the given arguments.
- apply_after_session_middlewares(self, *args, **kwargs) -> None: Applies the after_session method of each middleware instance to the given arguments.

Fields:
- middleware_list: List of middleware instances.
"""

@pytest.fixture
def mock_producer():
    mock_producer = MagicMock()
    return mock_producer


class TestMiddlewareManager:
    # # Tests that middleware_list is correctly initialized
    def test_initialize_middleware_list(self, mock_producer):
        middleware_list = [
            StatsMiddleware(mock_producer, "foo_topic", {}),
            SpiderStatusMiddleware("1.2.3", "http://localhost:8000", "valid_token"),
            RequestsHistoryMiddleware(mock_producer, "foo_topic", {},)
        ]
        middleware_manager = MiddlewareManager(middleware_list)
        assert middleware_manager.middleware_list == middleware_list

    def test_stats_updated_correctly_after_apply_session_middlewares(self, mock_producer):
        with patch("requests.patch", return_value=MagicMock(status_code=200)):
            stats = {}
            middleware_list = [
                StatsMiddleware(mock_producer, "foo_topic", {}, stats),
                SpiderStatusMiddleware(
                    "1.2.3", "http://localhost:8000", "valid_token", stats),
                RequestsHistoryMiddleware(mock_producer, "foo_topic", {})
            ]
            middleware_manager = MiddlewareManager(middleware_list)
            middleware_manager.apply_before_session_middlewares()
            middleware_manager.apply_after_session_middlewares()
            date_format = r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}.\d{3}$'
            assert re.match(date_format, stats["start_time"])
            assert re.match(date_format, stats["finish_time"])
            fields_to_check = ['start_time', 'finish_time', 'elapsed_time_seconds',
                                'finish_reason', 'memusage/startup', 'memusage/max', 'log_count/INFO',
                                'log_count/WARNING', 'log_count/ERROR', 'downloader/request_count',
                                'downloader/response_count', 'downloader/response_bytes', 'response_received_count']
            for field in fields_to_check:
                assert field in stats

    def test_stats_updated_correctly_after_apply_all_middlewares(self, mock_producer):
        with patch("requests.patch", return_value=MagicMock(status_code=200)):
            stats = {}
            middleware_list = [
                StatsMiddleware(mock_producer, "foo_topic", {}, stats),
                SpiderStatusMiddleware("1.2.3", "http://localhost:8000", "valid_token", stats),
                RequestsHistoryMiddleware(mock_producer, "foo_topic", {})
                # Note the order of middlewares is important
            ]
            middleware_manager = MiddlewareManager(middleware_list)
            middleware_manager.apply_before_session_middlewares()
            middleware_manager.apply_before_request_middlewares("GET")
            middleware_manager.apply_before_request_middlewares("POST")
            req = MagicMock(spec=EstelaHttpRequest)
            req.method = "GET"
            success_response = EstelaResponse('http://test.com', b'test', 'test', 200, req, 4, 'test', timedelta(seconds=2))
            middleware_manager.apply_after_request_middlewares(success_response)
            middleware_manager.apply_after_request_middlewares(success_response)
            middleware_manager.apply_after_session_middlewares()
            date_format = r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}.\d{3}$'
            assert re.match(date_format, stats["start_time"])
            assert re.match(date_format, stats["finish_time"])
            fields_to_check = ['start_time', 'finish_time', 'elapsed_time_seconds',
                                'finish_reason', 'memusage/startup', 'memusage/max', 'log_count/INFO',
                                'log_count/WARNING', 'log_count/ERROR', 'downloader/request_count',
                                'downloader/response_count', 'downloader/response_bytes', 'response_received_count']
            for field in fields_to_check:
                assert field in stats
            assert stats["downloader/request_count"] == 2
            assert stats["downloader/request_method_count/GET"] == 1
            assert stats["downloader/request_method_count/POST"] == 1
            assert stats["finish_reason"] == "Finished"
            assert stats["response_received_count"] == 2


    def test_stats_updated_correctly_after_apply_spider_status_middleware(self, mock_producer):
        with patch("requests.patch", return_value=MagicMock(status_code=200)):
            stats = {}
            middleware_list = [
                SpiderStatusMiddleware("1.2.3", "http://localhost:8000", "valid_token", stats),
            ]
            middleware_manager = MiddlewareManager(middleware_list)
            middleware_manager.apply_before_session_middlewares()
            middleware_manager.apply_before_request_middlewares("GET")
            middleware_manager.apply_before_request_middlewares("POST")
            req = MagicMock(spec=EstelaHttpRequest)
            req.method = "GET"
            success_response = EstelaResponse('http://test.com', b'test', 'test', 200, req, 4, 'test', timedelta(seconds=2))
            middleware_manager.apply_after_request_middlewares(success_response)
            middleware_manager.apply_after_request_middlewares(success_response)
            middleware_manager.apply_after_session_middlewares()
            assert not stats
            assert requests.patch.call_count == 2