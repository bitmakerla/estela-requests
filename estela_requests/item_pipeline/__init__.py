"""Basic Item Pipeline."""
from abc import ABC, abstractmethod

from typing import Dict

class ItemPipelineInterface:

    @abstractmethod
    def process_item(self, item):
        pass
