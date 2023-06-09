"""Basic Item Pipeline."""
from typing import Dict
from estela_requests.estela_hub import EstelaHub
from estela_queue_adapter.abc_producer import ProducerInterface

class ItemPipeline:
    def __init__(self, 
                 producer: ProducerInterface,
                 topic: str,
                 metadata: dict,
                 ) -> None:
        self.producer = producer
        self.metadata = metadata
        self.topic = topic

    @classmethod
    def from_estela_hub(cls, estela_hub: EstelaHub):
        return cls(estela_hub.producer, estela_hub.job_items_topic, {"jid": estela_hub.job})
        
    def process_item(self, item: Dict) -> Dict:
        return item
    
    def send_item(self, item: Dict, *args, **kwargs):
        parsed_item = self.process_item(item)
        self.producer.send(self.topic, {
            **self.metadata,
            "payload": parsed_item,
        })
