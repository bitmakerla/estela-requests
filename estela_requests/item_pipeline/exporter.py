from abc import abstractclassmethod, abstractmethod

from estela_queue_adapter.abc_producer import ProducerInterface


class ItemExporterInterface:  # Change to feedstorage?

    @abstractclassmethod
    def from_estela_hub(cls, estela_hub):
        pass

    @abstractmethod
    def export_item(self, item: dict, *args, **kwargs):
        pass

class StdoutItemExporter(ItemExporterInterface):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def from_estela_hub(cls, estela_hub):
        return cls()

    def export_item(self, item):
        print(f"Item: {item}")


class KafkaItemExporter(ItemExporterInterface):

    def __init__(self,
                producer: ProducerInterface,
                metadata: dict,
                topic: str,
                stats: dict
        ) -> None:
        self.stats = stats
        self.producer = producer
        self.metadata = metadata
        self.topic = topic

    @classmethod
    def from_estela_hub(cls, estela_hub):
        return cls(estela_hub.producer, {"jid": estela_hub.job}, estela_hub.job_items_topic, estela_hub.stats)

    def export_item(self, item: dict):
        self.stats["item_scraped_count"] = self.stats.get("item_scraped_count", 0) + 1
        self.producer.send(self.topic, {
             **self.metadata,
             "payload": item,
         })

class ItemExporterManager:
    def __init__(self, item_exporter_list: list[ItemExporterInterface]) -> None:
        self.item_exporter_list = item_exporter_list

    @classmethod
    def from_estela_hub(cls, estela_hub):
        item_exporter_cls_list: list[type[ItemExporterInterface]] = estela_hub.item_exporters
        item_exporter_list = []
        for item_exporter_cls in item_exporter_cls_list:
            item_exporter_list.append(item_exporter_cls.from_estela_hub(estela_hub))
        return cls(item_exporter_list)

    def export_item(self, item):
        for item_exporter in self.item_exporter_list:
            item_exporter.export_item(item)
