import logging

from estela_requests.request_interfaces import RequestsInterface
from estela_queue_adapter.get_interface import get_producer_interface
from estela_requests.middlewares.requests_history import RequestsHistoryMiddleware
from estela_requests.middlewares.spider_status import SpiderStatusMiddleware
from estela_requests.middlewares.stats import StatsMiddleware
from estela_requests.item_pipeline.exporter import KafkaItemExporter, StdoutItemExporter

ESTELA_PRODUCER = None
HTTP_CLIENT = RequestsInterface()
ESTELA_ITEM_PIPELINES = []
ESTELA_ITEM_EXPORTERS = [StdoutItemExporter]
ESTELA_NOISY_LIBRARIES = ["requests", "urllib3", "charset_normalizer"]
ESTELA_LOG_LEVEL = logging.DEBUG
ESTELA_MIDDLEWARES = []
HTTP_CLIENT = RequestsInterface()
ESTELA_LOG_FLAG = 'default'
JOB_STATS_TOPIC = ""
JOB_ITEMS_TOPIC = ""
JOB_REQUESTS_TOPIC = ""
JOB_LOGS_TOPIC = ""
ESTELA_API_HOST = ""
ESTELA_SPIDER_JOB = ""
ESTELA_SPIDER_ARGS = ""
ESTELA_AUTH_TOKEN = ""