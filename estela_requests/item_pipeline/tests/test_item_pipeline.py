from unittest.mock import MagicMock

from estela_queue_adapter.abc_producer import ProducerInterface

from estela_requests.item_pipeline.default import MyItemPipeline
from estela_requests.item_pipeline.manager import ItemPipelineManager


class TestItemPipeline:

    def test_default_pipeline(self):
        MagicMock(spec=ProducerInterface)
        pipeline = MyItemPipeline()
        my_item = {"foo": "bar"}
        parsed_item = pipeline.process_item(my_item)
        assert parsed_item == my_item

    def test_pipeline_manager(self):
        pipeline = MyItemPipeline()
        manager = ItemPipelineManager([pipeline])
        my_item = {"foo": "bar"}
        parsed_item = manager.process_item(my_item)
        assert parsed_item == my_item
