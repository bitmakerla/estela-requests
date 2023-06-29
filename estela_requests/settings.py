import logging

from estela_requests.request_interfaces import RequestsInterface
from estela_queue_adapter.get_interface import get_producer_interface
from estela_requests.middlewares.requests_history import RequestsHistoryMiddleware
from estela_requests.middlewares.spider_status import SpiderStatusMiddleware
from estela_requests.middlewares.stats import StatsMiddleware
from estela_requests.item_pipeline.exporter import KafkaItemExporter, StdoutItemExporter

ESTELA_PRODUCER = get_producer_interface()
ESTELA_PRODUCER.get_connection()
HTTP_CLIENT = RequestsInterface()
ESTELA_API_HOST = "http://127.0.0.1"
ESTELA_SPIDER_JOB = "101.madbymike.4796d37b-698b-4684-83c8-e3763c8d32ba"
ESTELA_SPIDER_ARGS = ""
ESTELA_ITEM_PIPELINES = []
ESTELA_ITEM_EXPORTERS = [KafkaItemExporter]
ESTELA_LOG_LEVEL = logging.DEBUG
ESTELA_MIDDLEWARES = [RequestsHistoryMiddleware, StatsMiddleware, SpiderStatusMiddleware]
JOB_STATS_TOPIC = "job_stats"
JOB_ITEMS_TOPIC = "job_items"
JOB_REQUESTS_TOPIC = "job_requests"
JOB_LOGS_TOPIC = "job_logs"
