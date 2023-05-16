"""Middleware to collect stats about the requests made by the spider."""

from typing import Dict
from estela_queue_adapter.abc_producer import ProducerInterface
from estela_requests_wrapper.middlewares.interface import EstelaMiddlewareInterface
from estela_requests_wrapper.http import EstelaResponse

class StatsMiddleware(EstelaMiddlewareInterface):

    def __init__(self, producer: ProducerInterface,
                 topic: str,
                 metadata: Dict) -> None:
        self.producer = producer
        self.topic = topic
        self.metadata = metadata
        self.stats = {}

    def after_request(self, response: EstelaResponse, *args, **kwargs):
        self.stats["downloader/request_count"] = self.stats.get("downloader/request_count", 0) + 1
        self.stats["downloader/request_method_count/{}".format(response.request.method)] = self.stats.get(
            "downloader/request_method_count/{}".format(response.request.method), 0) + 1
        self.stats["downloader/response_status_count/{}".format(response.status_code)] = self.stats.get(
            "downloader/response_status_count/{}".format(response.status_code), 0) + 1
    
    def after_session(self, *args, **kwargs):
        self.producer.send(self.topic, {
            **self.metadata,
            "payload": self.stats,
        })
    
    def before_request(self, *args, **kwargs):
        return super().before_request(*args, **kwargs)
    
    def before_session(self, *args, **kwargs):
        return super().before_session(*args, **kwargs)
