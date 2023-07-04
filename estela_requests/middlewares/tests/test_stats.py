# Generated partially by CodiumAI
import random
from unittest.mock import Mock

import pytest
from estela_queue_adapter.abc_producer import ProducerInterface

from estela_requests.estela_http import EstelaResponse
from estela_requests.middlewares.stats import StatsMiddleware

"""
Code Analysis

Main functionalities:
The StatsMiddleware class is responsible for collecting statistics about the spider's performance and sending them to the Estela platform. It implements the EstelaMiddlewareInterface and defines methods to collect statistics before and after each request and session. It also defines a default set of statistics to be collected and sent to the platform.

Methods:
- __init__: initializes the StatsMiddleware object with a producer, topic, metadata, and default statistics.
- from_estela_hub: creates a StatsMiddleware object from an EstelaHub object.
- after_request: collects statistics after each request, such as the response status code, count, and size.
- after_session: collects statistics after each session, such as the finish time, elapsed time, and finish reason. Sends the collected statistics to the Estela platform.
- before_request: collects statistics before each request, such as the request count and method count.
- before_session: collects statistics before each session, such as the start time.

Fields:
- producer: a ProducerInterface object used to send statistics to the Estela platform.
- topic: a string representing the topic to which the statistics will be sent.
- metadata: a dictionary containing metadata about the spider job.
- stats: a dictionary containing the collected statistics.
- default_data: a dictionary containing the default set of statistics to be collected.
"""
class TestStatsMiddleware:
    # Tests that after_request method updates stats correctly
    def test_stats_updates_correctly(self):
        
        producer = Mock(spec=ProducerInterface)
        topic = 'test_topic'
        metadata = {'jid': 'test_job'}
        stats = {}
        middleware = StatsMiddleware(producer, topic, metadata, stats)
        request_count = random.randint(1, 10)
        for _ in range(request_count):
            middleware.before_request("GET")
        success_response = EstelaResponse('http://test.com', b'test', 'test', 200, None, 4, 'test', 2.0)
        failed_response =  EstelaResponse('http://test.com', b'test', 'test', 401, None, 4, 'test', 2.0)
        middleware.after_request(success_response) 
        middleware.after_request(failed_response) 
        middleware.after_request(failed_response) 
        assert middleware.stats['downloader/response_status_count/200'] == 1
        assert middleware.stats['downloader/response_status_count/401'] == 2
        assert middleware.stats['downloader/response_count'] == 3
        assert middleware.stats['downloader/response_bytes'] == (3 * len(b'test'))
        assert middleware.stats['response_received_count'] == 3
        assert middleware.stats['downloader/request_count'] == request_count

    # Tests that after_session method updates stats correctly
    def test_after_session_updates_stats_correctly(self):
        producer = Mock(spec=ProducerInterface)
        topic = 'test_topic'
        metadata = {'jid': 'test_job'}
        stats = {}
        middleware = StatsMiddleware(producer, topic, metadata, stats)
        middleware.stats['start_time'] = '01/01/2022 00:00:00.000'
        middleware.stats['finish_time'] = '01/01/2022 00:00:02.000'
        middleware.after_session()
        assert middleware.stats['elapsed_time_seconds'] == 2.0
        assert middleware.stats['finish_reason'] == 'Finished'
        assert middleware.stats['downloader/request_count'] == 0
        assert middleware.stats['response_received_count'] == 0

    def test_after_session_updates_stats_correctly(self):
        producer = Mock(spec=ProducerInterface)
        topic = 'test_topic'
        metadata = {'jid': 'test_job'}
        stats = {}
        middleware = StatsMiddleware(producer, topic, metadata, stats)
        middleware.before_session()
        assert middleware.stats["start_time"]

    # Tests that default_data dictionary is correctly assigned to instance variable
    def test_session_default_data_is_correctly_assigned(self):
        producer = Mock(spec=ProducerInterface)
        topic = 'test_topic'
        metadata = {'key': 'value'}
        stats = {}        
        middleware = StatsMiddleware(producer, topic, metadata, stats)
        middleware.before_session()
        assert middleware.stats["start_time"]
        middleware.after_session()
        assert middleware.stats["finish_time"]
        assert middleware.stats["finish_reason"] == "Finished"
        assert set(middleware.stats.keys()) == set(middleware.default_data)

    def test_before_request_updates_stats_correctly(self):
        producer = Mock(spec=ProducerInterface)
        topic = 'test_topic'
        metadata = {'key': 'value'}
        stats = {}        
        middleware = StatsMiddleware(producer, topic, metadata, stats)
        middleware.before_request("GET")
        middleware.before_request("GET")
        middleware.before_request("POST")
        middleware.before_request("PUT")
        assert middleware.stats["downloader/request_count"] == 4
        assert middleware.stats["downloader/request_method_count/GET"] == 2
        assert middleware.stats["downloader/request_method_count/POST"] == 1
        assert middleware.stats["downloader/request_method_count/PUT"] == 1

    def test_after_request_updates_stats_correctly(self):
        producer = Mock(spec=ProducerInterface)
        topic = 'test_topic'
        metadata = {'key': 'value'}
        stats = {}        
        middleware = StatsMiddleware(producer, topic, metadata, stats)
        success_response = EstelaResponse('http://test.com', b'test', 'test', 200, None, 4, 'test', 2.0)
        failed_response =  EstelaResponse('http://test.com', b'test', 'test', 401, None, 4, 'test', 2.0)
        middleware.after_request(success_response)
        middleware.after_request(success_response)
        middleware.after_request(success_response)
        middleware.after_request(failed_response)
        assert middleware.stats["downloader/response_status_count/200"] == 3
        assert middleware.stats["downloader/response_status_count/401"] == 1
        assert middleware.stats["downloader/response_count"] == 4
        assert middleware.stats["response_received_count"] == 4
