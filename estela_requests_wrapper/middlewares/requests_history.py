from estela_queue_adapter import get_producer_interface
from estela_requests_wrapper.estela_response import EstelaResponse

class RequestsHistoryMiddleware:
    # It should be executed by request.
    """It will send requests history to the queue producer."""
    def __init__(self, response: EstelaResponse, producer, topic) -> None:
        self.response = response
        self.producer = producer
        self.topic = topic
    
    def get_history_data(self):
        return {
            "url": self.response.url,
            "status": int(self.response.status),
            "method": self.response.request.method,
            "duration": int(self.response.request.time_in_seconds),
            #"time": time.time(),
            "self.response_size": len(self.response.body),
            "fingerprint": self.response.request.fingerprint,
        }
    
    def send_data_to_queue(self):
        self.producer.send(self.topic, self.get_history_data())
