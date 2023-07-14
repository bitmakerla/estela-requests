from datetime import timedelta
from unittest.mock import ANY, MagicMock, Mock, patch

import requests
from estela_queue_adapter.abc_producer import ProducerInterface
from requests import Response

from estela_requests import EstelaRequests
from estela_requests.estela_http import EstelaHttpRequest
from estela_requests.item_pipeline.default import MyItemPipeline
from estela_requests.item_pipeline.exporter import (
    ItemExporterManager,
    KafkaItemExporter,
    StdoutItemExporter,
)
from estela_requests.item_pipeline.manager import ItemPipelineManager
from estela_requests.middlewares.manager import MiddlewareManager
from estela_requests.middlewares.requests_history import RequestsHistoryMiddleware
from estela_requests.middlewares.spider_status import SpiderStatusMiddleware
from estela_requests.middlewares.stats import StatsMiddleware
from estela_requests.request_interfaces import RequestsInterface


class TestEstelaRequests:

    @staticmethod
    def get_mock_item(response):
        """Simulating using response to get a item."""
        # parse response
        return {"foo": "bar"}

    def test_estela_requests_run(self, capsys):
        producer_mock = Mock(spec=ProducerInterface)
        requests_topic = "foo_requests"
        stats_topic = "foo_stats"
        item_topic = "foo_item"
        metadata = {"jid": "1.2.3"}
        stats = {}
        middleware_list = [
            RequestsHistoryMiddleware(producer_mock, requests_topic, metadata),
            StatsMiddleware(producer_mock, stats_topic, metadata, stats),
            SpiderStatusMiddleware("1.2.3", "http://mock_host.example", "mock_token", stats),
        ]
        pp_list = [
            MyItemPipeline()
        ]
        ex_list = [
            StdoutItemExporter(),
            KafkaItemExporter(producer_mock, metadata, item_topic, stats),
        ]
        mw_manager = MiddlewareManager(middleware_list)
        pp_manager = ItemPipelineManager(pp_list)
        ex_manager = ItemExporterManager(ex_list)
        req_obj = MagicMock(spec=EstelaHttpRequest)
        req_obj.method = "GET"
        response = MagicMock(spec=Response)
        response.url = 'http://example.com'
        response.content = b'example content'
        response.text = 'example content'
        response.status_code = 200
        response.request = req_obj
        response.elapsed = timedelta(seconds=2)
        req_itf = Mock(spec=RequestsInterface)
        req_itf.request.return_value = response
        with patch("requests.patch"):
            estela_request = EstelaRequests(mw_manager, pp_manager, ex_manager, req_itf)
            fin_response = estela_request.get("http://example.com") # It should call all the middlewares.
            item = self.get_mock_item(fin_response)
            expected_output = f"Item: {item}\n"
            estela_request.send_item(item)
            estela_request.cleanup_estela_requests()
            assert requests.patch.call_count == 2 # Called once with RUNNING and once with COMPLETED
            assert producer_mock.send.call_count == 3 # Called three times(StatsMw, RequestsMw, ItemExporter)
            requests.patch.assert_called_with(
                'http://mock_host.example/api/projects/3/spiders/2/jobs/1',
                data=ANY, headers={'Authorization': 'Token mock_token'}, timeout=20)
            requests.patch.assert_called_with(
                'http://mock_host.example/api/projects/3/spiders/2/jobs/1',
                data={'status': 'COMPLETED', 'lifespan': ANY, 'total_response_bytes': 15, 'item_count': 1, 'request_count': 1},
                headers={'Authorization': 'Token mock_token'},
                timeout=20,
            )
            producer_mock.send.assert_any_call(requests_topic, {
                'jid': '1.2.3',
                'payload': {
                    'url': 'http://example.com',
                    'status': 200,
                    'method': "GET",
                    'duration': ANY,
                    'time': ANY,
                    'fingerprint': ANY,
                    'response_size': 15,
                }
            })
            producer_mock.send.assert_any_call(item_topic, {
                'jid': '1.2.3',
                "payload":{
                    **item,
                }
            })
            producer_mock.send.assert_any_call(stats_topic, {
                "jid": "1.2.3",
                "payload": {
                    "start_time": ANY,
                    "downloader/request_count": 1,
                    "downloader/request_method_count/GET": 1,
                    "downloader/response_status_count/200": 1,
                    "downloader/response_count": 1,
                    "downloader/response_bytes": 15,
                    "response_received_count": 1,
                    "item_scraped_count": 1,
                    "finish_time": ANY,
                    "finish_reason": "Finished",
                    "memusage/startup": None,
                    "memusage/max": None,
                    "log_count/INFO": 0,
                    "log_count/WARNING": 0,
                    "log_count/ERROR": 0,
                    "elapsed_time_seconds": ANY,
                }
            })
            captured = capsys.readouterr().out
            assert captured == expected_output


