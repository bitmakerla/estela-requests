"""Given a list of item pipeline list it will apply all the pipelines in a given order."""


from estela_requests.estela_hub import EstelaHub
from estela_requests.item_pipeline import ItemPipelineInterface


class ItemPipelineManager:
    def __init__(self,
                item_pipeline_list: list[ItemPipelineInterface]
        ) -> None:
        self.item_pipeline_list = item_pipeline_list

    @classmethod
    def from_estela_hub(cls, estela_hub: EstelaHub):
        item_pipeline_cls_list: list[type[ItemPipelineInterface]] = estela_hub.item_pipelines
        item_pipeline_list = []
        for item_pipeline_cls in item_pipeline_cls_list:
            item_pipeline_list.append(item_pipeline_cls())
        return cls(item_pipeline_list)

    def process_item(self, item):
        parsed_item = item
        for item_pipeline in self.item_pipeline_list:
            parsed_item = item_pipeline.process_item(item)
        return parsed_item
