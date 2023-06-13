from estela_requests.request_interfaces import RequestsInterface
from estela_queue_adapter.get_interface import get_producer_interface
from estela_requests.middlewares.requests_history import RequestsHistoryMiddleware
from estela_requests.middlewares.spider_status import SpiderStatusMiddleware
from estela_requests.middlewares.stats import StatsMiddleware

ESTELA_PRODUCER = get_producer_interface()
ESTELA_PRODUCER.get_connection()
HTTP_CLIENT = RequestsInterface()
ESTELA_API_HOST = "http://127.0.0.1"
ESTELA_SPIDER_JOB = "777.publicidad.4796d37b-698b-4684-83c8-e3763c8d32ba"
ESTELA_SPIDER_ARGS = ""
ESTELA_MIDDLEWARES = [SpiderStatusMiddleware, RequestsHistoryMiddleware, StatsMiddleware]
JOB_STATS_TOPIC = "job_stats"
JOB_ITEMS_TOPIC = "job_items"
JOB_REQUESTS_TOPIC = "job_requests"
