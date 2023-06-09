from estela_requests.request_interfaces import RequestsInterface
from estela_queue_adapter.get_interface import get_producer_interface
from estela_requests.middlewares.requests_history import RequestsHistoryMiddleware
from estela_requests.middlewares.spider_status import SpiderStatusMiddleware
from estela_requests.middlewares.stats import StatsMiddleware

ESTELA_PRODUCER = get_producer_interface()
ESTELA_PRODUCER.get_connection()
HTTP_CLIENT = RequestsInterface()
ESTELA_API_HOST = "http://127.0.0.1"
ESTELA_SPIDER_JOB = "999.lucy.b1709e50-6717-4913-af4c-49b72a8243f5"
ESTELA_SPIDER_ARGS = ""
ESTELA_MIDDLEWARES = [SpiderStatusMiddleware, RequestsHistoryMiddleware, StatsMiddleware, StatsMiddleware]
JOB_STATS_TOPIC = "job_stats"
JOB_ITEMS_TOPIC = "job_items"
JOB_REQUESTS_TOPIC = "job_requests"
AUTH_TOKEN = "d2ce7ee727b023f51cd185b9ab4078b573c90f15"
