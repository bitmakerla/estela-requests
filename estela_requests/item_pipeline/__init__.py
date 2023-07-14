"""Basic Item Pipeline."""
from abc import abstractmethod


class ItemPipelineInterface:

    @abstractmethod
    def process_item(self, item):
        pass
