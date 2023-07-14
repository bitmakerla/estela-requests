from unittest.mock import MagicMock

from estela_queue_adapter.abc_producer import ProducerInterface

from estela_requests.item_pipeline.exporter import (
    ItemExporterManager,
    KafkaItemExporter,
    StdoutItemExporter,
)


class TestItemPipeline:

    def test_kafka_exporter(self):
        producer = MagicMock(spec=ProducerInterface)
        stats = {}
        exporter = KafkaItemExporter(producer, {"jid": "test"}, "test", stats)
        mock_item = {}
        for _ in range(10):
            exporter.export_item(mock_item)
        assert stats["item_scraped_count"] == 10
        producer.send.assert_any_call('test', {'jid': 'test', 'payload': {}})

    def test_stdout_export_item_prints_correct_output(self, capsys):
        item = {'name': 'John', 'age': 30}
        expected_output = f"Item: {item}\n"
        exporter = StdoutItemExporter()
        exporter.export_item(item)
        captured = capsys.readouterr()
        assert captured.out == expected_output

    def test_item_exporter_manager(self, capsys):
        item = {'name': 'John', 'age': 30}
        expected_output = f"Item: {item}\n"
        producer = MagicMock(spec=ProducerInterface)
        stats = {}
        exporter_list = [KafkaItemExporter(producer, {"jid": "test"}, "test", stats),StdoutItemExporter()]
        exporter_manager = ItemExporterManager(exporter_list)
        exporter_manager.export_item(item)
        assert stats["item_scraped_count"] == 1
        captured = capsys.readouterr()
        assert captured.out == expected_output
        producer.send.assert_called_once_with('test', {'jid': 'test', 'payload': item})
