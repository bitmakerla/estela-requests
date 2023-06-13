"""Basic Item Pipeline."""
from typing import Dict
from estela_requests.estela_hub import EstelaHub
from estela_queue_adapter.abc_producer import ProducerInterface

class ItemPipeline:
    def __init__(self, 
                 producer: ProducerInterface,
                 topic: str,
                 metadata: dict,
                 stats: dict = {}
                 ) -> None:
        self.producer = producer
        self.metadata = metadata
        self.topic = topic
        self.stats = stats

    @classmethod
    def from_estela_hub(cls, estela_hub: EstelaHub):
        return cls(estela_hub.producer, estela_hub.job_items_topic, {"jid": estela_hub.job}, estela_hub.stats)
        
    def process_item(self, item: Dict) -> Dict:
        return item
    
    def send_item(self, item: Dict, *args, **kwargs):
        parsed_item = self.process_item(item)
        self.stats["item_scraped_count"] = self.stats.get("item_scraped_count", 0 ) + 1
        self.producer.send(self.topic, {
            **self.metadata,
            "payload": parsed_item,
        })
