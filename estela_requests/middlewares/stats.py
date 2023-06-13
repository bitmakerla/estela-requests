"""Middleware to collect stats about the requests made by the spider."""

from typing import Dict
from estela_queue_adapter.abc_producer import ProducerInterface
from estela_requests.middlewares.interface import EstelaMiddlewareInterface
from estela_requests.estela_hub import EstelaHub
from estela_requests.estela_http import EstelaResponse
from estela_requests.utils import elapsed_seconds_time, parse_time

class StatsMiddleware(EstelaMiddlewareInterface):

    def __init__(self, producer: ProducerInterface,
                 topic: str,
                 metadata: Dict,
                 stats: Dict = {}
                 ) -> None:
        self.producer = producer
        self.topic = topic
        self.metadata = metadata
        self.stats = stats
        self.default_data = {
            "log_count/INFO": None,
            "memusage/startup": None,
            "memusage/max": None,
            "scheduler/enqueued/memory": None,
            "scheduler/enqueued": None,
            "scheduler/dequeued/memory": None,
            "scheduler/dequeued": None,
            "log_count/WARNING": None,
            "downloader/response_count": None,
            "downloader/response_bytes": None,
            "log_count/ERROR": None,
            "httpcompression/response_bytes": None,
            "httpcompression/response_count": None,
            "response_received_count": None,
            "request_depth_max": None,
            "httperror/response_ignored_count": None,
            "elapsed_time_seconds": None,
            "finish_time": None,
            "finish_reason": None
        }

    @classmethod
    def from_estela_hub(cls, estela_hub: EstelaHub):
        return cls(estela_hub.producer, estela_hub.job_stats_topic, {"jid": estela_hub.job}, estela_hub.stats)

    def after_request(self, response: EstelaResponse, *args, **kwargs):
        self.stats["downloader/response_status_count/{}".format(response.status_code)] = self.stats.get(
            "downloader/response_status_count/{}".format(response.status_code), 0) + 1
        self.stats["downloader/response_bytes"] = self.stats.get("downloader/response_bytes", 0) + len(response.text)
    
    def after_session(self, *args, **kwargs):
        self.stats["finish_time"] = self.stats.get("finish_time", parse_time())
        self.stats["elapsed_time_seconds"] =  elapsed_seconds_time(self.stats["finish_time"], self.stats["start_time"])
        for k, v in self.default_data.items():
            if k not in self.stats:
                self.stats[k] = v
        self.producer.send(self.topic, {
            **self.metadata,
            "payload": self.stats,
        })
    
    def before_request(self, method, *args, **kwargs):
        self.stats["downloader/request_count"] = self.stats.get("downloader/request_count", 0) + 1
        self.stats["downloader/request_method_count/{}".format(method)] = self.stats.get(
            "downloader/request_method_count/{}".format(method), 0) + 1
        return super().before_request(*args, **kwargs)
    
    def before_session(self, *args, **kwargs):
        self.stats["start_time"] = self.stats.get("start_time", parse_time())
        return super().before_session(*args, **kwargs)
