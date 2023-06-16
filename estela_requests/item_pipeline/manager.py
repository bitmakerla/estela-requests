"""Given a list of item pipeline list it will apply all the pipelines in a given order."""
from typing import List, Type

from estela_requests.item_pipeline import ItemPipelineInterface
from estela_requests.estela_hub import EstelaHub
from estela_queue_adapter.abc_producer import ProducerInterface

class ItemPipelineManager:  # TODO: this is an specific Kafka pipeline manager.
    def __init__(self,
                item_pipeline_list: List[ItemPipelineInterface],
                producer: ProducerInterface,
                metadata: dict,
                topic: str,
                stats: dict
        ):
        self.item_pipeline_list = item_pipeline_list
        self.stats = stats
        self.producer = producer
        self.metadata = metadata
        self.topic = topic

    @classmethod
    def from_estela_hub(cls, estela_hub: EstelaHub):
        itme_pipeline_cls_list: List[Type[ItemPipelineInterface]] = estela_hub.item_pipelines
        item_pipeline_list = []
        for item_pipeline_cls in itme_pipeline_cls_list:
            item_pipeline_list = item_pipeline_cls()
        return cls(item_pipeline_list, estela_hub.producer, {"jid": estela_hub.job}, estela_hub.job_items_topic, estela_hub.stats)
    
    def process_item(self, item):
        parsed_item = item
        for item_pipeline in self.item_pipeline_list:
            parsed_item = item_pipeline.process_item()
        return parsed_item
    
    def send_item(self, item, *args, **kwargs):
        parsed_item = self.process_item(item)
        self.stats["item_scraped_count"] = self.stats.get("item_scraped_count", 0) + 1
        # self.producer.send(self.topic, {
        #     **self.metadata,
        #     "payload": parsed_item,
        # }) 
