from typing import Dict
from estela_queue_adapter.abc_producer import ProducerInterface
from estela_requests_wrapper.estela_response import EstelaResponse
from estela_requests_wrapper.utils import parse_time
from estela_requests_wrapper.middlewares.interface import EstelaMiddlewareInterface


class RequestsHistoryMiddleware(EstelaMiddlewareInterface):
    # It should be executed by request.
    """It will send requests history to the queue producer."""

    def __init__(self, producer: ProducerInterface,
                 topic: str,
                 metadata: Dict) -> None:
        self.producer = producer
        self.topic = topic
        self.metadata = metadata
    
    def get_history_data(self, response: EstelaResponse):
        return {
            **self.metadata,
            "payload":{ 
                "url": response.url,
                "status": int(response.status),
                #"method": response.request.method,
                #"duration": response.request.time_in_seconds,
                "time": parse_time(),
                #"fingerprint": response.request.fingerprint,
                "fingerprint": "dumps",
                "self.response_size": len(response.body),
            }
        }

    def after_request(self, response: EstelaResponse):
        self.producer.send(self.topic, self.get_history_data(response))