
from estela_queue_adapter.abc_producer import ProducerInterface

from estela_requests.estela_http import EstelaResponse
from estela_requests.estela_hub import EstelaHub
from estela_requests.middlewares.interface import EstelaMiddlewareInterface
from estela_requests.utils import parse_time


class RequestsHistoryMiddleware(EstelaMiddlewareInterface):
    """It will send requests history to the queue producer."""

    def __init__(self,
                 producer: ProducerInterface,
                 topic: str,
                 metadata: dict[str, str],
                 )-> None:
        self.producer = producer
        self.topic = topic
        self.metadata = metadata

    @classmethod
    def from_estela_hub(cls, estela_hub: EstelaHub):
        return cls(estela_hub.producer, estela_hub.job_requests_topic, {"jid": estela_hub.job})

    def get_history_data(self, response: EstelaResponse):
        return {
            **self.metadata,
            "payload":{
                "url": response.url,
                "status": int(response.status_code),
                "method": response.request.method,
                "duration": response.time_in_seconds.total_seconds(),
                "time": parse_time(),
                "fingerprint": response.fingerprint,
                "response_size": len(response.text),
            }
        }

    def after_request(self, response: EstelaResponse, *args, **kwargs):
        self.producer.send(self.topic, self.get_history_data(response))

    def before_request(self, *args, **kwargs):
        return super().before_request(*args, **kwargs)

    def after_session(self, *args, **kwargs):
        return super().after_session(*args, **kwargs)

    def before_session(self, *args, **kwargs):
        return super().before_session(*args, **kwargs)
